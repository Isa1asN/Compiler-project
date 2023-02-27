import sys
import os
from antlr4 import *
from graphviz import Digraph
from antlr_tools.C_GrammarListener import C_GrammarListener

# AST (Abstract Syntax Tree) class for creating a tree structure for the C code
class AST:

	def __init__(self, name="", value=None, nodeType=None):
		self.parent = None
		self.children = list()
		self.name = name
		self.value = value
		self.type = nodeType
		self.childIndex = 0
		self.graph = None

	def __str__(self):
		return self.name + f" | {self.value}" * (self.value is not None) + f" | {self.type}" * (self.type is not None)

	# add a child node to the current node
	def addChild(self, name="", value=None, nodeType=None):
		newNode = AST(name, value, nodeType)
		newNode.parent = self
		self.children.append(newNode)

	# get a child node by index
	def getChild(self, index):
		return self.children[index]

	# get the current child node
	def getCurrentChild(self):
		if(len(self.children) != 0):
			return self.children[self.childIndex]

		return None

	# increment child index
	def incrementChildIndex(self):
		self.childIndex += 1

	# get the number of child nodes
	def getChildCount(self):
		return len(self.children)

	# create a Graphviz dot node
	def createDotNode(self, nodeIndex, node):
		self.graph.node(str(nodeIndex), str(node))

		currentIndex = nodeIndex
		for i in range(len(node.children)):
			self.graph.edge(str(nodeIndex), str(currentIndex + i + 1))
			currentIndex = self.createDotNode(currentIndex + i + 1, node.getChild(i))

		return currentIndex

	# create a Graphviz dot file for the AST
	def to_dot(self, filename):
		self.graph = Digraph(name = filename, node_attr={'shape': 'box'})

		self.createDotNode(0, self)

		# print(self.graph.source)
		filename = "dotfiles/" + os.path.basename(filename) + "_AST.dot"
		file = open(filename, "w+")
		file.write(self.graph.source)
		file.close()


# GrammarListener class for parsing the C code and creating an AST
class GrammarListener(C_GrammarListener):

	def __init__(self):
		super().__init__()
		self.AST_Root = None
		self.currentNode = None

	# create the root node of the AST
	def enterStart(self, ctx):
		root = AST("Root")
		self.AST_Root = root
		self.currentNode = root

		# Add include child if present
		if ctx.INCLUDE() != None:
			self.currentNode.addChild("include", ctx.INCLUDE().getText())
			self.currentNode.incrementChildIndex()

		# Add function children
		for i in range(len(ctx.function())):
			self.currentNode.addChild()

		# Add global var children
		for i in range(len(ctx.global_var())):
			self.currentNode.addChild()

		# Add EOF child
		self.currentNode.addChild("EOF")

	# set the current node to the next child node for a global variable declaration
	def enterGlobal_var(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = ctx.identifier().getText()
		self.currentNode.type = ctx.type_name().getText()

		if ctx.types() is not None:
			self.currentNode.value = ctx.types().getText()

	def exitGlobal_var(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterFunction(self, ctx):
		# fill in function node
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "function"
		self.currentNode.value = ctx.identifier()[0].getText()
		if ctx.VOID() is None:
			self.currentNode.type = ctx.type_name()[0].getText()
		else:
			self.currentNode.type = "void"

		# create children
		# create argument children
		for i in range(1, len(ctx.type_name())):
			self.currentNode.addChild("argument", ctx.identifier()[i].getText(), ctx.type_name()[i].getText())
			self.currentNode.incrementChildIndex()

		# create statement child
		self.currentNode.addChild()

	def exitFunction(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterCodeBlock(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "code block"

		# create children
		for child in ctx.statement():
			self.currentNode.addChild()

	def exitCodeBlock(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterFirstCodeBlock(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "code block"

		# create children
		for child in ctx.statement():
			self.currentNode.addChild()

	def exitFirstCodeBlock(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterIfStat(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "if"

		# create condition child
		self.currentNode.addChild()

		# create statement child
		self.currentNode.addChild()

		# in case of Else, add child
		if ctx.ELSE() is not None:
			self.currentNode.addChild()		

	def exitIfStat(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterWhileStat(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "while"

		# create condition child
		self.currentNode.addChild()

		# create statement child
		self.currentNode.addChild()	

	def exitWhileStat(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterForStat(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "while"

		for i in range(4):
			self.currentNode.addChild()
			
	def exitForStat(self, ctx):
		parent = self.currentNode.parent
		# move the decl/ass to the parent
		parent.children.insert(parent.childIndex, self.currentNode.getChild(0))
		parent.getChild(parent.childIndex).parent = parent
		parent.incrementChildIndex()
		self.currentNode.children.pop(0)

		# increment/decrement to the codeblock
		last_statement = self.currentNode.getChild(1)
		codeBlock = self.currentNode.getChild(2)
		codeBlock.children.append(last_statement)
		codeBlock.children[-1].parent = codeBlock
		self.currentNode.children.pop(1)

		self.currentNode = parent
		self.currentNode.incrementChildIndex()

	def enterReturn(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "return"

		# create return expression child
		self.currentNode.addChild()

	def exitReturn(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterBasicAss(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "="

		if ctx.PLUS() is not None:
			self.currentNode.value = "+"
		elif ctx.MIN() is not None:
			self.currentNode.value = "-"
		elif ctx.MULT() is not None:
			self.currentNode.value = "*"
		elif ctx.DIV() is not None:
			self.currentNode.value = "/"
		
		# create left term child
		self.currentNode.addChild()

		# create right term child
		self.currentNode.addChild()

	def exitBasicAss(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterArrayDecl(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "array decl"
		self.currentNode.value = ctx.identifier().getText()
		self.currentNode.type = ctx.type_name().getText();

		for i in range(len(ctx.all_right()) + len(ctx.both_expr())):
			self.currentNode.addChild()

		for c in range(len(ctx.getText())):
			if(ctx.getText()[c] == "[" and ctx.getText()[c + 1] != "]"):
				self.currentNode.getChild(0).name = "array length"

	def exitArrayDecl(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()		

	def enterCompExpr(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = ctx.compare().getText()

		# create left term child
		self.currentNode.addChild()

		# create right term child
		self.currentNode.addChild()

	def exitCompExpr(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()		

	def enterPlusArith(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "+"

		self.currentNode.addChild()
		self.currentNode.addChild()

	def exitPlusArith(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterMinArith(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "-"

		self.currentNode.addChild()
		self.currentNode.addChild()

	def exitMinArith(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterMultTerm(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "*"

		self.currentNode.addChild()
		self.currentNode.addChild()

	def exitMultTerm(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterDivTerm(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "/"

		self.currentNode.addChild()
		self.currentNode.addChild()

	def exitDivTerm(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterArrayExpr(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "array"
		self.currentNode.value = ctx.identifier().getText()

		# Check if array value is dereferenced/depointered
		if ctx.AMP() is not None:
			self.currentNode.name = "array address"
		elif ctx.MULT() is not None:
			self.currentNode.name = "array value"

		if self.currentNode.parent.name == "=" and self.currentNode.parent.type is None:
			self.currentNode.parent.type = "ass"

		# create index child
		self.currentNode.addChild()

	def exitArrayExpr(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterFuncExpr(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.name = "f call"
		self.currentNode.value = ctx.identifier().getText()

		# create argument children
		for i in range(len(ctx.all_right())):
			self.currentNode.addChild("argument")

		for i in range(len(ctx.both_expr())):
			self.currentNode.addChild("argument")

		# for i in range(1, len(ctx.type_name())):
		# 	self.currentNode.addChild("argument", ctx.identifier()[i].getText(), ctx.type_name()[i].getText())
		# 	self.currentNode.incrementChildIndex()

	def exitFuncExpr(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()		

	def enterTypeValue(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		if ctx.MIN() is not None:
			self.currentNode.value = "-" + ctx.types().getText()
		else:
			self.currentNode.value = ctx.types().getText()

		if ctx.types().identifier() is not None:
			self.currentNode.name = "identifier"

			if ctx.types().AMP() is not None:
				self.currentNode.value = ctx.types().getText()[1:]
				self.currentNode.name = "address"
			elif ctx.types().MULT() is not None:
				self.currentNode.value = ctx.types().getText()[1:]
				self.currentNode.name = "value"
			else:
				self.currentNode.value = ctx.types().getText()
		else:
			if self.currentNode.name != "array length":
				self.currentNode.name = "constant"

				if ctx.types().FLOAT() is not None:
					self.currentNode.type = "float"
				elif ctx.types().INT() is not None:
					self.currentNode.type = "int"
				elif ctx.types().CHAR_T() is not None:
					self.currentNode.type = "char"
				elif ctx.types().STRING() is not None:
					self.currentNode.type = "char*"

	def exitTypeValue(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterTypeID(self, ctx):
		self.currentNode = self.currentNode.getCurrentChild()
		self.currentNode.value = ctx.identifier().getText()

		if ctx.type_name() is not None:
			self.currentNode.type = ctx.type_name().getText()
			if self.currentNode.parent.name != "code block":
				self.currentNode.parent.type = "decl"
		else:
			self.currentNode.parent.type = "ass"
			self.currentNode.name = "identifier"

	def exitTypeID(self, ctx):
		self.currentNode = self.currentNode.parent
		self.currentNode.incrementChildIndex()

	def enterEos(self, ctx):
		self.currentNode.incrementChildIndex()

	def enterStEos(self, ctx):
		self.currentNode.children.remove(self.currentNode.getCurrentChild())
