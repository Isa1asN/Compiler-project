import AST
from enum import Enum, auto
from SymbolTableGenerator import UndeclaredException

class Liveness(Enum):
	LIVE = auto()
	DEAD = auto()
	UNDEF = auto()

class LivenessControl:

	def __init__(self, symbolTable):
		self.symbolTable = symbolTable
		self.currentSymbolTable = symbolTable.root
		self.currentSymbolTable.childIndex = len(self.currentSymbolTable.children) - 1

	def getLiveness(self, varName, symbolTable):
		try:
			return symbolTable.liveDict[varName]
		except KeyError:
			return Liveness.UNDEF

	def traverse(self, currentASTNode):
		"""Traverses an AST node using DFS to find all variables and set them to LIVE"""
		stack = [currentASTNode]

		while len(stack) != 0:
			currentASTNode = stack.pop()

			if currentASTNode.name in ["identifier", "array", "value", "address"] :
				self.climb(currentASTNode.value, self.currentSymbolTable)

			stack.extend(currentASTNode.children)

	def climb(self, varName, symbolTable):
		"""Climbs the symboltables until it finds the one with the correct variable used
			varName: the variable to find
			symbolTable: the symboltable to start at"""

		liveness = self.getLiveness(varName, symbolTable)
		if varName in symbolTable.symbols:
			# the variable was found in the current scope
			# now check if the variable was defined in the current scope before the current line
			if varName in symbolTable.declaredDict:
				self.climb(varName, symbolTable.parent)
			else:
				symbolTable.liveDict[varName] = Liveness.LIVE

		else:
			#symbolTable.liveDict[varName] = Liveness.LIVE
			self.climb(varName, symbolTable.parent)

	def evaluateWhile(self, assNode):
		"""Climbs up the AST to check wether the variable is in a while loop.
			If it is, it does some stuff"""

		searchVar = assNode.getChild(0).value
		parent = assNode
		searchLimit = assNode
		foundWhile = False

		while(parent.name != "Root" and not foundWhile):
			parent = parent.parent
			foundWhile = (parent.name == "while")
			for i in range(parent.children.index(searchLimit)):
				currentNode = parent.getChild(i)
				if currentNode.type == "decl":
					if currentNode.getChild(0).value == searchVar:
						break
				# "" for declaration without definition
				elif currentNode.name == "":
					if currentNode.value == searchVar:
						break
				elif currentNode.name == "array decl":
					if currentNode.value == searchVar:
						break
			searchLimit = parent

		# if this flag is True, a while was found and the variable was not redeclared
		if foundWhile:
			stack = [parent.getChild(0)]
			while len(stack) != 0:
				currentNode = stack.pop()
				if currentNode.name in ["identifier", "array", "value", "address"] :
					if currentNode.value == searchVar:
						return True

				stack.extend(currentNode.children)

		return False

	def checkLiveness(self, AST, dropCode=True):
		stack = list()
		codeBlocks = [-1]
		currentDepth = 0

		stack.append((AST, 0))

		while len(stack) != 0:
			currentASTNode, currentDepth = stack.pop()
			currentName = currentASTNode.name

			if currentName == "Root":
				for child in currentASTNode.children:
					if child.name == "function":
						stack.append((child.getChild(0), 1))

			else:
				if codeBlocks[-1] >= currentDepth:
					self.currentSymbolTable = self.currentSymbolTable.parent
					self.currentSymbolTable.childIndex -= 1
					codeBlocks.pop()

				if currentName == "code block":
					codeBlocks.append(currentDepth)
					self.currentSymbolTable = self.currentSymbolTable.getCurrentChild()
					self.currentSymbolTable.childIndex = len(self.currentSymbolTable.children) - 1
					stack.extend([(x, currentDepth + 1) for x in currentASTNode.children])

				elif currentName == "while":
					stack.append((currentASTNode.getChild(0), currentDepth + 1))
					# set the currrent depth of the codeblock to 1 less because the codeblock will increment on its own
					stack.append((currentASTNode.getChild(1), currentDepth))

				elif currentName == "if":
					stack.append((currentASTNode.getChild(0), currentDepth + 1))
					for child in currentASTNode.children[1:]:
						stack.append((child, currentDepth))

				elif currentName == "=":
					leftChild = currentASTNode.getChild(0)
					rightChild = currentASTNode.getChild(1)
					if self.getLiveness(leftChild.value, self.currentSymbolTable) == Liveness.LIVE:
						self.traverse(rightChild)
						self.currentSymbolTable.liveDict[leftChild.value] = Liveness.DEAD
						if currentASTNode.type == "decl":
							self.currentSymbolTable.declaredDict[leftChild.value] = True
						continue
					elif currentASTNode.type == "ass":
						if self.evaluateWhile(currentASTNode):
							self.traverse(rightChild)
							self.currentSymbolTable.liveDict[leftChild.value] = Liveness.DEAD
							continue

					if dropCode:
						currentASTNode.parent.children.remove(currentASTNode)
					print("\033[0;33mWARNING: variable {} is never used\033[0m".format(leftChild.value))

				elif currentName == "return":
					self.traverse(currentASTNode)

				# for condition check in 'if', 'while'
				elif currentName in ["==", "!=", "<", "<=", ">", ">="]:
					self.traverse(currentASTNode) 

				elif currentName == "f call":
					self.traverse(currentASTNode)


		self.symbolTable.clearChildIndices()
