
curr = 0

def readFile(filename):
	"""Reads a file, removing any excess whitespace and comment lines beginning with '#'"""
	KB = []
	lines = [line.rstrip('\n') for line in open(filename)] # Strip newlines from file and read into list
	lines = [line.rstrip() for line in lines if not line.startswith('#') and line] # filter out empty lines and comment lines and strip trailing whitespace
	lines = [line.lstrip() for line in lines] # strip leading whitespace
	lines = [" ".join(line.split()) for line in lines] # Seperate expression term in clause by exactly one space
	for line in lines:
		parsedLine = parse(line)
		if parsedLine is not None:
			KB.append(parsedLine) # Parse, format, and standardize variables in each line
		else:
			print("ERROR:", line, "could not be added to the KB!")
			print("Is it properly formatted?")
	KB = removeDuplicates(KB) # Remove duplicate entries from KB
	return KB

def parse(line):
	"""Parses a FOL expression, formatting predicates as strings and rules as lists of strings"""
	newList = []

	# If the input line is missing outer parentheses, attempt to format it correctly
	if not line.startswith('((') or not line.endswith('))'):
		line = '(' + line + ')'

	rule = False
	for i in range(1, len(line) - 2): # Search in the outermost set of parentheses
		string = ""
		if line[i] is '(': # Find the next innermost set of parentheses and copy it's contents into 'string'
			j = i + 1
			while j < len(line) - 2 and line[j] is not ')':
				string += line[j]
				j += 1

			# If we've broken out of the first interior parentheses and we aren't at the outermost closing parentheses, it's a rule
			if j < len(line) - 2 or rule:
				rule = True # Make sure we know it's a rule on subsequent iterations
				newList = newList + [string] # Add fact as new list element
			else:
				newList = string # If it's not a rule, then just return it as a string
				break

	if len(newList) == 0: # If any kind of anomaly was encountered parsing the line, return None
		return

	newList = standardize(newList, {}) # Standardize variables

	return newList


def removeDuplicates(KB):
	"""Removes duplicate entries from a KB"""
	unique_KB = []
	for expression in KB:
		if expression not in unique_KB:
			unique_KB.append(expression)
	return unique_KB	


def standardize(expression, theta):
	"""Standardizes variable names in a FOL KB to prevent confusing behavior and enhance clarity"""
	if isinstance(expression, list): # If expression is a rule
		return_list = []
		for term in expression:
			return_list.append(standardize_string(term, theta)) # Standardize each element
		return return_list
	else: # Otherwise
		to_return = standardize_string(expression, theta) # Standardize fact
		return to_return

def standardize_string(expression, theta):
	"""Helper function for standardize; standardizes a single string of input"""
	global curr # Use global counter to keep track of current variable number

	to_return = ""
	for word in expression.split(): # For words in the input string
		if word.startswith("?"): # If the word is a variable
			if word not in theta: # If the variable has not yet been encountered in this expression
				theta[word] = "?v" + str(curr) #  Assign it a new number
				curr += 1
			to_return += " " + theta[word] # Add the new variable to the string
		else:
			to_return += " " + word # If the word is not a variable, add it to the new string with no changes
	return " ".join(to_return.rstrip().split()) # Keep standard spacing and formatting

def ask(KB, query):
	"""Retrieve information from Knowledge Base. 
	Utilizes backward chaining to make complex inferences about the contents of the KB"""
	query = parse(query) # Format and standardize query

	if isinstance(query, list): #If the query has multiple conditions, all of them must be met
		results = ask_and(KB, query, {})
	else:
		results = ask_or(KB, query, {})

	try: # Try reading the first of the results from the query
		temp = next(results)
		temp = subst(query, temp)
		if temp == query: # If the result is the same as the query (the query was not in terms of a variable) 
			yield True # return 'True' since the query was entailed by the KB
			return
		else: # If the query was not a yes or no question, yield the first result
			yield temp
	except StopIteration: # If results is empty, the query was not entailed
		yield "This query cannot be inferred with the given KB"
		return

	for result in results: # Yield each subsequent result
		answer = subst(query, result)
		yield answer


def ask_or(KB, query, theta):
	"""Uses backwards chaining to determines if a single query is entailed by the KB"""
	for expression in KB: # Check all expressions for those that may entail the query
		if isinstance(expression, list): # If the expression is a rule
			unifier = unify(expression[len(expression) - 1], query, theta) 
			if unifier is not None: # Check if the result unifies with the query
				if theta != unifier:
					for result in ask_and(KB, expression[:len(expression) - 1], unifier): # Check to see if antecedents can be entailed
						yield result
				#else:
					#yield unifier
		else:
			unifier = unify(expression, query, theta) # If the expression is not a rule, see if it unifies with the query
			if unifier is not None: 
				yield unifier


def ask_and(KB, antecedents, theta):
	"""Uses backward chaining to determine if a set of antecedents (or queries) is entailed by the KB"""
	if theta is None:
		return
	elif len(antecedents) == 0:
		yield theta
	else:
		for theta1 in ask_or(KB, antecedents[0], theta): # Check if the first term is entailed, then check the rest
			for theta2 in ask_and(KB, antecedents[1:], theta1):
				yield theta2


def subst(expression, unifier):
	"""Substitutes variables in an expression with other variables or ground instances using a unifier"""
	if isinstance(expression, list): # If result is a rule, substitute each term
		return_list = []
		for term in expression:
			return_list.append(subst_string(term, unifier))
		return return_list
	else: # Otherwise, substitute term
		return subst_string(expression, unifier)


def subst_string(expression, unifier):
	"""Helper function for subst; Substitutes variables in a string with ground instances or other variables using a unifier"""
	to_return = ""
	for word in expression.split(): # For each word in the expression, determine if it's a variable
		if word.startswith("?"):
			if word in unifier: # If it's in the unifier
				to_return += " " + unifier[word] # Append the translated variable to a string
		else:
			to_return += " " + word # If it's not a variable, append the word with no changes
	return " ".join(to_return.rstrip().split()) # Keep standard spacing and formatting


def unify(x, y, theta): 
	"""Unifies two expressions in FOL if they are unifiable"""
	if isinstance(x, list): # Separate by individual words in the expressions
		x = " ".join(x)
	if isinstance(y, list):
		y = " ".join(y)

	x = x.split()
	y = y.split()
	return unify_main(x, y, theta) # Call the main unification algorithm


def unify_main(x, y, theta):
	"""Helper function for unify; Unifies two expressions in FOL if they are unifiable"""
	if theta is None: # Check for failure
		return
	elif x == y: # Check if the tokens are equal
		return theta
	elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y): # If unifying lists
		return unify_main(x[1:], y[1:], unify_main(x[0], y[0], theta)) # Unify the first element, and then the rest
	elif isinstance(x, list) or isinstance(y, list): # If there is a discrepancy with the lengths of the expressions, return failure
		return
	elif x.startswith('?'): # If x or y is a variable, unify them
		return unify_var(x, y, theta)
	elif y.startswith('?'):
		return unify_var(y, x, theta)
	else:
		return # Otherwise return failure


def unify_var(var, x, theta):
	"""Helper function for unify_main; Unifies two variables"""
	new_theta = dict(theta) # Copy theta to prevent unwanted modification
	if var in theta: # If var is already in the unifier
		return unify_main(theta[var], x, theta) # Substitute it and call unify again 
	elif x in theta: #Same with x
		return unify_main(var, theta[x], theta)
	else: # If neither var nor x is in the unifier, add var and return the new unifier
		new_theta[var] = x
		return new_theta