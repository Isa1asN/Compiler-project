from graphviz import Digraph
import os

# define a custom exception for semantic errors
class SemanticException(Exception):
    # the __init__ method initializes the class instance with an error message
	def __init__(self, message):
		super().__init__("\033[91m{}\033[0m".format(message))
# define custom exceptions for specific semantic errors
class RedeclarationException(SemanticException):

	def __init__(self, var):
		super().__init__("{} is redeclared in the same scope".format(var))

class UndeclaredException(SemanticException):

	def __init__(self, var):
		super().__init__("{} was not declared".format(var))

class ReturnException(SemanticException):

	def __init__(self, func):
		super().__init__("return in void function {}()".format(func))

class NoReturnException(SemanticException):

	def __init__(self, func):
		super().__init__("no return in non-void function {}()".format(func))

class NoMainException(SemanticException):

	def __init__(self):
		super().__init__("no main() function present")

# define a symbol table class for storing and manipulating symbol tables
class SymbolTable:

    # define a TableNode class for representing nodes in the symbol table tree
	class TableNode:

        # the __init__ method initializes the TableNode instance with a parent node, a depth, and a name
		def __init__(self, parent, depth, name):
			self.children = list()
			self.childIndex = 0
			self.parent = parent
			self.depth = depth
			self.name = name
			self.graph = None

			self.symbols = dict()
			self.registerDict = dict()
			self.symbolLength = dict()

			# used by LivenessControl
			self.liveDict = dict()
			self.declaredDict = dict()

        # the getCurrentChild method returns the current child node
		def getCurrentChild(self):
			if(len(self.children) != 0):
				return self.children[self.childIndex]

			return None
		
        # the incrementChildIndex method increments the child index
		def incrementChildIndex(self):
			self.childIndex += 1

        # the getSymbolType method returns the type of a given symbol
		def getSymbolType(self, symbol, varFound=True):
			search_node = self
			if varFound == False:
				search_node = self.parent
			while symbol not in search_node.symbols:
				search_node = search_node.parent
				if search_node is None:
					raise UndeclaredException(symbol)
			return search_node.symbols[symbol]
		
        # the getSymbolRegister method returns the register of a given symbol
		def getSymbolRegister(self, symbol, varFound=True):
			search_node = self
			if varFound == False:
				search_node = self.parent
			while symbol not in search_node.registerDict:
				search_node = search_node.parent
				if search_node is None:
					raise UndeclaredException(symbol)
			return search_node.registerDict[symbol]
		
        # the getSymbolLength method returns the length of a given symbol
		def getSymbolLength(self, symbol, varFound=True):
			search_node = self
			if varFound == False:
				search_node = self.parent
			while symbol not in search_node.symbolLength:
				search_node = search_node.parent
				if search_node is None:
					raise UndeclaredException(symbol)
			return search_node.symbolLength[symbol]

		def createDotNode(self, nodeIndex, node):
			self.graph.node(str(nodeIndex), str(node))

			currentIndex = nodeIndex
			for i in range(len(node.children)):
				self.graph.edge(str(nodeIndex), str(currentIndex + i + 1))
				currentIndex = self.createDotNode(currentIndex + i + 1, node.children[i])

			return currentIndex

		def __str__(self):
			html_table = "<<TABLE BORDER='0' CELLBORDER='1' CELLSPACING='0' CELLPADDING='4'><TR><TD COLSPAN='3'>{}</TD></TR>".format(self.name)
			for name, var_type in self.symbols.items():
				register = ""
				if name in self.registerDict:
					register = self.registerDict[name]
				html_table += "<TR><TD>{}</TD><TD>{}</TD><TD>{}</TD></TR>".format(var_type, name, register)
			html_table += "</TABLE>>"
			return html_table

		def to_dot(self, filename):
			self.graph = Digraph(name = "Symbol Table", node_attr={'shape': 'plaintext'})

			self.createDotNode(0, self)

			#print(self.graph.source)
			filename = "dotfiles/" + os.path.basename(filename) + "_SymbolTable.dot"
			file = open(filename, "w+")
			file.write(self.graph.source)
			file.close()

	def __init__(self):
		self.root = self.TableNode(None, 0, "Root")
		self.current_node = self.root

	def clearChildIndices(self):
		path = [self.root]
		while len(path) != 0:
			current_node = path.pop()
			current_node.childIndex = 0
			path.extend(current_node.children)

	def fill_tree(self, AST):
		# use DFS to traverse the AST and construct the symbol table tree
		path = []
		current_depth = 0

		main_present = False
		for child in AST.children:
			if child.name == "function":
				# check if there is a main() function present
				if child.value == "main":
					main_present = True

				# check for returns
				returns = self.returns(child.getChild(-1))
				if returns and child.type == "void":
					raise ReturnException(child.value)
				elif not returns and child.type != "void":
					raise NoReturnException(child.value)

			if child.name == "include":
				self.current_node.symbols["printf"] = "int"
				self.current_node.symbols["scanf"] = "int"

				# global variable definitions
			if child.name != "function" and child.name != "include" and child.name != "EOF":
				if child.name == "array decl":	
					self.current_node.symbols[child.value] = child.type
				else:
					self.current_node.symbols[child.name] = child.type
			else:
				path.append((child, 1))

		if not main_present:
			raise NoMainException()

		path.reverse()

		while len(path) != 0:
			current_ast_node, current_depth = path.pop()
			current_name = current_ast_node.name

			if current_name != "Root":
				# climb up the symbol tree if needed
				while current_depth <= self.current_node.depth:
					self.current_node = self.current_node.parent

			# in future: for loop requires an extra scope (upper scope -> for scope -> code_block scope)
			# create new table for each new scope entered
			if current_name == "code block":
				new_node = self.TableNode(self.current_node, current_depth, current_name)
				self.current_node.children.append(new_node)
				self.current_node = new_node

				# add function arguments to the code block scope below
				if current_ast_node.parent.name == "function":
					for argument in current_ast_node.parent.children[:-1]:
						self.current_node.symbols[argument.value] = argument.type
			else:
				# fill the current symbol table
				# skip arguments because they are already handled when entering a codeblock
				if current_ast_node.name != "argument" and current_ast_node.name != "constant" and current_ast_node.name != "=":
					if current_ast_node.value is not None and current_ast_node.type is not None:
						if current_ast_node.value in self.current_node.symbols:
							raise RedeclarationException(current_ast_node.value)
						self.current_node.symbols[current_ast_node.value] = current_ast_node.type

				# verify if a variable being used was defined beforehand
				if current_ast_node.name == "identifier" or current_ast_node.name == "f call":
					self.current_node.getSymbolType(current_ast_node.value)


			# reverse the children so the first child will get popped first
			path.extend([(x, current_depth + 1) for x in current_ast_node.children][::-1])

	def returns(self, ast_node):
		for child in ast_node.children:
			if child.name == "if":
				returns = self.returns(child.getChild(1))
				if not returns:
					continue

				if len(child.children) == 3:
					returns = self.returns(child.getChild(2))
					if not returns:
						continue

				return True

			elif child.name == "return":
				return True

		return False

	def to_dot(self, filename):
		self.root.to_dot(filename)