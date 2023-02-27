import SymbolTableGenerator
from AST import AST
import operator
import re
import sys

class MIPSGenerator:

	def __init__(self, AST, SymbolTable):
		self.datastring = ""
		self.textstring = ""
		self.globalstring = ""
		self.tempstring = ""
		self.AST = AST
		self.SymbolTable = SymbolTable
		self.stringCounter = 0
		self.labelCounter = 0
		self.floatingPointCounter = 0
		self.currentFunction = ""
		self.current_symboltable = SymbolTable.root
		self.functionDict = dict()
		self.globalStackCounter = 0
		self.arithmeticChild = "left"
		self.currentDepth = 0
		self.currentOpNode = None

	def writeToFile(self, filename):
		file = open(filename, "w+")
		file.write(self.datastring + "\n" + self.textstring)
		file.close()
		# return self.datastring + "\n" + self.textstring

	def incrementFunctionStackCounter(self):
		self.functionDict[self.currentFunction] += 4

	def getNewLabel(self):
		label = "L" + str(self.labelCounter)
		self.labelCounter += 1
		return label

	def incrementGlobalStackCounter(self):
		self.globalStackCounter += 4

	def loadIntoRegister(self, regType, regNo, loadReg, address=False):
		register = "${}{}".format(regType, regNo)
		if register != loadReg:
			instruction = "lw"
			if address:
				instruction = "la"
			if regType == "f":
				instruction = "l.s"
			self.textstring += "\t{} {}, {}\n".format(instruction, register, loadReg)

		return register

	def findDeclaration(self, searchVar):
		parent = self.currentOpNode.parent
		for i in range(parent.children.index(self.currentOpNode)):
			currentNode = parent.getChild(i)
			if currentNode.type == "decl":
				if currentNode.getChild(0).value == searchVar:
					return True
			# "" for declaration without definition
			elif currentNode.name == "":
				if currentNode.value == searchVar:
					return True
			elif currentNode.name == "array decl":
				if currentNode.value == searchVar:
					return True

		# if the variable was not found in the current scope, check the function arguments
		for rootChild in self.AST.children:
			if rootChild.value == self.currentFunction:
				for i in range(self.SymbolTable.root.symbolLength[self.currentFunction]):
					if rootChild.getChild(i).value == searchVar:
						return True
		return False

	def generateStringConst(self, function, string):
		register = "{}.str{}".format(function, self.stringCounter)
		self.datastring += "{}: .asciiz {}\n".format(register, string)
		self.stringCounter += 1
		return register, "data", "char*"

	def typeCast(self, inputType, outputType, inputVarType, inputReg, outputReg):
		if (inputType == "int" and outputType == "char") or (inputType == "char" and outputType == "int"):
			return inputReg, inputVarType, inputType

		elif outputType == "float":			
			if inputVarType == "const":
				self.textstring += "\tli $t7, {}\n".format(inputReg)
				inputReg = "$t7"
			elif inputVarType == "identifier":
				self.textstring += "\tlw $t7, {}\n".format(inputReg)
				inputReg = "$t7"

			self.textstring += "\tmtc1 {}, $f{}\n".format(inputReg, outputReg)
			self.textstring += "\tcvt.s.w $f{}, $f{}\n".format(outputReg, outputReg)

			return "$f{}".format(outputReg), "register", "float"

		else:
			if inputVarType == "data" or inputVarType == "identifier":
				self.textstring += "\tl.s $f7, {}\n".format(inputReg)
				inputReg = "$f7"

			self.textstring += "\ttrunc.w.s $f7, {}\n".format(inputReg)
			self.textstring += "\tmfc1 $t{}, $f7\n".format(outputReg)
			

			return "$t{}".format(outputReg), "register", "int"
		

	def generateTypeCast(self, leftReg, leftType, leftVarType, rightReg, rightType, rightVarType, leftOutputReg, rightOutputReg):
		if leftType == "float" and rightType != "float":
			if leftVarType == "data":
				leftReg = self.loadIntoRegister("f", leftOutputReg, leftReg, True)
				leftVarType = "register"
			elif leftVarType == "identifier":
				leftReg = self.loadIntoRegister("f", leftOutputReg, leftReg)
				leftVarType = "register"
			rightReg, rightType, rightVarType = self.typeCast(rightType, "float", rightVarType, rightReg, rightOutputReg)

		elif leftType != "float" and rightType == "float":
			if rightVarType == "data":
				rightReg = self.loadIntoRegister("f", rightOutputReg, rightReg, True)
				rightVarType = "register"
			elif rightVarType == "identifier":
				rightReg = self.loadIntoRegister("f", rightOutputReg, rightReg)
				rightVarType = "register"
			leftReg, leftVarType, leftType = self.typeCast(leftType, "float", leftVarType, leftReg, leftOutputReg)

		return leftReg, leftType, leftVarType, rightReg, rightType, rightVarType

	def generate(self):
		"""Main function that starts the entire code generation"""

		self.datastring += "\t.data\n"

		for child in self.AST.children:
			if child.name == "include":
				continue
			if child.name == "function":
				self.currentFunction = child.value
				self.generateFunction(child)
			elif child.name == "array decl":
				self.generateArrayDeclaration(child, "global")
			elif child.name == "EOF":
				continue
			else:
				self.generateGlobalDeclaration(child)

	def generateFunction(self, current_ast_node):
		"""Generates the code for a function declaration/definition"""
		if current_ast_node.value == "main":
			self.tempstring = self.textstring
			self.textstring = ""

		totalArguments = len(current_ast_node.children) - 1;
		self.current_symboltable.symbolLength[current_ast_node.value] = totalArguments

		self.current_symboltable = self.current_symboltable.getCurrentChild()
		for i in range(totalArguments):
			self.current_symboltable.registerDict[current_ast_node.getChild(i).value] = "{}.ph.{}($sp)".format(current_ast_node.value, current_ast_node.getChild(i).value)
		self.current_symboltable = self.current_symboltable.parent

		if current_ast_node.getChild(-1).name == "code block":
			self.functionDict[current_ast_node.value] = 0
			self.textstring += "\n{}:\n".format(current_ast_node.value)
			self.textstring += "\taddiu $sp, $sp, -$stackcounter_ph\n\tsw $ra, 0($sp)\n"
			self.incrementFunctionStackCounter()
			self.currentFunction = current_ast_node.value
			self.generateCodeBlock(current_ast_node.getChild(-1))

		self.textstring += "\n{}.exit:\n".format(self.currentFunction)
		self.textstring += "\tlw $ra, 0($sp)\n\taddiu $sp, $sp, {}\n".format(self.functionDict[self.currentFunction])

		if self.currentFunction == "main":
			self.textstring += "\tli $v0, 10\n\tsyscall\n"

			self.textstring = "\t.text\n" + self.globalstring + self.textstring + self.tempstring

		else:
			self.textstring += "\tjr $ra\n"

	def generateCodeBlock(self, current_ast_node):
		# Starting code block
		self.currentDepth += 1
		self.current_symboltable = self.current_symboltable.getCurrentChild()

		for child in current_ast_node.children:
			self.currentOpNode = child
			if child.name == "code block":
				self.generateCodeBlock(child)
			elif len(child.children) == 0 and child.type is not None:
				if child.name != "array decl":
					self.generateDeclaration(child)
				else:
					raise SymbolTableGenerator.SemanticException("Size of array {} was not declared".format(child.value))
			elif child.name == "=":
				# If left child has no type -> declaration
				if child.type == "decl":
					self.generateDefinition(child)
				# Else -> assignment
				elif child.type == "ass":
					self.generateAssignment(child)
			elif child.name == "f call":
				# the only rvalue that can be called on its own is a function call
				# all the others are essentially useless and are thus not generated
				self.generateExpression(child)
			elif child.name == "if":
				self.generateIfStatement(child)
			elif child.name == "while":
				self.generateWhileStatement(child)
			elif child.name == "array decl":
				self.generateArrayDeclaration(child)
			elif child.name == "return":
				self.generateReturn(child)
				break

		self.currentDepth -= 1
		# Ending code block
		# Check wether code block belongs to a function
		if current_ast_node.parent.name == "function":
			totalArguments = self.current_symboltable.getSymbolLength(self.currentFunction)

			newStackCounter = self.functionDict[self.currentFunction]
			self.textstring = self.textstring.replace("$stackcounter_ph", str(newStackCounter))

			for i in range(totalArguments):
				argName = current_ast_node.parent.getChild(i).value
				offset = (i * 4) + (self.functionDict[self.currentFunction])
				self.textstring = self.textstring.replace("{}.ph.{}".format(self.currentFunction, argName), str(offset))
				self.current_symboltable.registerDict[argName] = f"{offset}($sp)"

				# add the second offset if necessary (in case of using function argument in function call)
				matches = set(re.findall(f'{self.currentFunction}.aph.[0-9]+.{argName}', self.textstring))
				for match in matches:
					secondOffset = int(match.split('.')[2])
					self.textstring = self.textstring.replace(match, str(offset + secondOffset))



		self.current_symboltable = self.current_symboltable.parent
		self.current_symboltable.incrementChildIndex()

	def generateExpression(self, current_ast_node, resultReg="0", leftType=""):
		nodeName = current_ast_node.name
		nodeValue = current_ast_node.value
		nodeType = current_ast_node.type

		if nodeName == "constant":
			if nodeType == "int" and leftType != "float":
				return nodeValue, "const", "int"
			elif nodeType == "char" and leftType != "float":
				return nodeValue, "const", "char"

			elif nodeType == "float" or leftType == "float":
				register = "{}.fp{}".format(self.currentFunction, self.floatingPointCounter)
				self.floatingPointCounter += 1
				self.datastring += "{}: .float {}\n".format(register, nodeValue)
				return register, "data", "float"

			elif nodeType == "char*":
				return self.generateStringConst(self.currentFunction, nodeValue)

		elif nodeName == "identifier":
			idType = self.current_symboltable.getSymbolType(nodeValue)
			return self.current_symboltable.getSymbolRegister(nodeValue, self.findDeclaration(nodeValue)), "identifier", idType

		elif nodeName == "address":
			self.textstring += "\tla $t4, {}\n".format(self.current_symboltable.getSymbolRegister(nodeValue), self.findDeclaration(nodeValue))
			return "$t4", "register", "address"

		elif nodeName == "array address":
			self.textstring += "\tla $t4, {}\n".format(self.current_symboltable.getSymbolRegister(nodeValue), self.findDeclaration(nodeValue))
			indexReg, indexVarType, indexType = self.generateExpression(current_ast_node.getChild(0))

			if indexVarType == "const":
				indexReg = str(int(indexReg) * 4)
				self.textstring += "\taddi $t4, $t4, {}\n".format(indexReg)

			elif indexVarType == "register" or indexVarType == "data" or indexVarType == "identifier":
				self.textstring += "\tli $t6, 4\n"
				if indexVarType == "data":
					self.textstring += "\tla $t5, {}\n".format(indexReg)
					self.textstring += "\tmul $t5, $t5, $t6\n"
				elif indexVarType == "identifier":
					self.textstring += "\tlw $t5, {}\n".format(indexReg)
					self.textstring += "\tmul $t5, $t5, $t6\n"
				elif indexVarType == "register":
					self.textstring += "\tmul $t5, $t5, {}\n".format(indexReg)

				self.textstring += "\tadd $t4, $t4, $t5\n".format(indexReg)

			return "$t4", "register", "address"

		elif nodeName == "value":
			loadType = self.current_symboltable.getSymbolType(nodeValue, self.findDeclaration(nodeValue))

			self.textstring += "\tlw $t4, {}\n".format(self.current_symboltable.getSymbolRegister(nodeValue, self.findDeclaration(nodeValue)))
			if self.current_symboltable.getSymbolType(nodeValue, self.findDeclaration(nodeValue)) == "float*":
				self.textstring += "\tl.s $f4, ($t4)\n"
				return "$f4", "register", "float"
			else:
				self.textstring += "\tlw $t4, ($t4)\n"
				return "$t4", "register", "int"

		elif nodeName == "f call":
			if nodeValue == "printf":
				self.generatePrint(current_ast_node)
			elif nodeValue == "scanf":
				self.generateScan(current_ast_node)
			else:
				return self.generateFunctionCall(current_ast_node)

		elif nodeName == "array":
			addOp = "add"
			loadOp = "lw"
			reg = "t"
			returnType = "int"
			if self.current_symboltable.getSymbolType(nodeValue, self.findDeclaration(nodeValue)) == "float":
				reg = "f"
				addOp = "add.s"
				loadOp = "l.s"
				returnType = "float"

			arrayRegister = self.current_symboltable.getSymbolRegister(current_ast_node.value, self.findDeclaration(nodeValue))
			if arrayRegister[-5:] == "($gp)":
				self.textstring += "\tlw $t2, {}\n".format(arrayRegister)
			else:
				self.textstring += "\tla $t2, {}\n".format(arrayRegister)
			indexReg, indexVarType, indexType = self.generateExpression(current_ast_node.getChild(0))

			if indexVarType == "const":
				if indexReg[0] == "-":
					raise Exception("\033[91mArray index should be a positive integer\033[0m")
				indexReg = str(int(indexReg) * 4)
				self.textstring += "\t{} ${}{}, {}($t2)\n".format(loadOp, reg, resultReg, indexReg)
			else:
				if indexVarType == "data" or indexVarType == "identifier":
					tempReg = "${}{}".format(reg, str(int(resultReg) + 1))
					self.textstring += "\tlw {}, {}\n".format(tempReg, indexReg)
					self.textstring += "\tli $t6, 4\n"
					self.textstring += "\tmul {}, {}, $t6\n".format(tempReg, tempReg)
					indexReg = tempReg

				self.textstring += "\t{} ${}2, ${}2, {}\n".format(addOp, reg, reg, indexReg)
				self.textstring += "\t{} ${}{}, ($t2)\n".format(loadOp, reg, resultReg)

			return "${}{}".format(reg, resultReg), "register", returnType


		elif nodeName in ["+", "-", "*", "/"]:
			return self.generateArithmetic(current_ast_node)

		elif nodeName in ["==", "!=", "<", "<=", ">", ">="]:
			return self.generateCondition(current_ast_node)

	def generateDeclaration(self, current_ast_node):
		stackCounter = self.functionDict[self.currentFunction]
		self.current_symboltable.registerDict[current_ast_node.value] = "{}($sp)".format(stackCounter)
		self.incrementFunctionStackCounter()

	def generateGlobalDeclaration(self, current_ast_node):
		register = "{}($gp)".format(self.globalStackCounter)

		varType = "word"
		reg = "t"
		loadOp = "lw"
		storeOp = "sw"
		if current_ast_node.type == "float":
			varType = "float"
			reg = "f"
			loadOp = "l.s"
			storeOp = "s.s"
		elif current_ast_node.type == "char*":
			varType = "asciiz"
			loadOp = "la"

		value = None
		if current_ast_node.value is not None:
			value = current_ast_node.value

		self.datastring += "global.{}: .{} {}\n".format(current_ast_node.name, varType, value)

		self.current_symboltable.registerDict[current_ast_node.name] = register
		if value is not None:
			self.globalstring += "\n\t{} ${}0, global.{}\n".format(loadOp, reg, current_ast_node.name)
			self.globalstring += "\t{} ${}0, {}\n".format(storeOp, reg, register)

		self.incrementGlobalStackCounter()


	def generateDefinition(self, current_ast_node):
		leftChild = current_ast_node.getChild(0)
		rightChild = current_ast_node.getChild(1)

		register, varType, rightType = self.generateExpression(rightChild, "0", leftChild.type)
		leftType = leftChild.type

		stackCounter = self.functionDict[self.currentFunction]

		if rightChild.name != "address" and rightChild.name != "value":
			if rightType != leftType:
				register, varType, regType = self.typeCast(rightType, leftType, varType, register, "0")

		if leftChild.type == "int" or leftChild.type == "char":
			if varType == "const":
				self.textstring += "\tli $t0, {}\n".format(register)
			elif varType != "const" and register[0] != "$":
				self.textstring += "\tlw $t0, {}\n".format(register)
			
			if varType == "register":
				self.textstring += "\tsw {}, {}($sp)\n".format(register, stackCounter)
			else:
				self.textstring += "\tsw $t0, {}($sp)\n".format(stackCounter)

		elif leftChild.type == "float":
			if varType != "register":
				self.textstring += "\tl.s $f0, {}\n".format(register)

			if varType == "register":
				self.textstring += "\ts.s {}, {}($sp)\n".format(register, stackCounter)
			else:
				self.textstring += "\ts.s $f0, {}($sp)\n".format(stackCounter)

		elif leftChild.type == "char*":
			if varType == "data":
				self.textstring += "\tla $t0, {}\n".format(register)
				self.textstring += "\tsw $t0, {}($sp)\n".format(stackCounter)

			elif varType == "register":
				self.textstring += "\tsw {}, {}($sp)\n".format(register, stackCounter)

		elif leftChild.type == "int*" or leftChild.type == "float*":
			if varType == "const":
				self.textstring += "\tli $t0, {}\n".format(register)
			elif varType == "register":
				self.textstring += "\tla $t0, ({})\n".format(register)

			self.textstring += "\tsw $t0, {}($sp)\n".format(stackCounter)

		self.current_symboltable.registerDict[leftChild.value] = "{}($sp)".format(stackCounter)
		self.incrementFunctionStackCounter()

	def generateAssignment(self, current_ast_node):
		instructions =  {
							"+": "add",
							"-": "add",
							"*": "mul",
							"/": "div"
					    }

		leftChild = current_ast_node.getChild(0)
		rightChild = current_ast_node.getChild(1)

		register = self.current_symboltable.getSymbolRegister(leftChild.value)
		rightReg, varType, rightType = self.generateExpression(rightChild)
		leftType = self.current_symboltable.getSymbolType(leftChild.value)

		if rightChild.name != "address" or rightChild.name == "value":
			if rightType != leftType:
				rightReg, varType, regType = self.typeCast(rightType, leftType, varType, rightReg, "1")

		addOp = "add"
		storeOp = "sw"
		reg = "t"
		if leftType == "float":
			reg = "f"
			addOp = "add.s"
			storeOp = "s.s"

		# No operator assignment
		if current_ast_node.value is None:
			if varType == "data" or varType == "identifier":
				rightReg = self.loadIntoRegister(reg, "0", rightReg)
			elif varType == "address":
				rightReg = self.loadIntoRegister(reg, "0", rightReg, True)
			elif varType == "const":
				tempReg = "${}0".format(reg)
				self.textstring += "\tli {}, {}\n".format(tempReg, rightReg)
				rightReg = tempReg
			
			if leftChild.name == "array":
				self.textstring += "\tla $t1 {}.{}\n".format(self.currentFunction, leftChild.value)
				indexReg, indexVarType, indexType = self.generateExpression(leftChild.getChild(0))

				if indexVarType == "const":
					if indexReg[0] == "-":
						raise Exception("\033[91mArray index should be a positive integer\033[0m")
					indexReg = str(int(indexReg) * 4)
					self.textstring += "\t{} ${}0, {}($t1)\n".format(storeOp, reg, indexReg)
				else:
					self.textstring += "\t{} ${}1, ${}1, {}\n".format(addOp, reg, reg, indexReg)
					self.textstring += "\t{} ${}0, ($t1)\n".format(storeOp, reg)

			else:
				self.textstring += "\t{} {}, {}\n".format(storeOp, rightReg, register)

		else:
			instr = instructions[current_ast_node.value]
			if reg == "f":
				if instr == "mult":
					instr = instr[:-1]
				instr += ".s"

			leftReg = self.loadIntoRegister(reg, "0", register)

			if varType == "const":
				if current_ast_node.value == "+":
					instr += "i"
				elif rightReg[0] == "-" and current_ast_node.value == "-":
					rightReg = rightReg[1:]
				elif rightReg[0] != "-" and current_ast_node.value == "-":
					rightReg = "-" + rightReg

			elif varType == "data" or varType == "identifier":
				rightReg = self.loadIntoRegister(reg, "2", rightReg)

			self.textstring += "\t{} ${}0, {}, {}\n".format(instr, reg, leftReg, rightReg)
			self.textstring += "\t{} ${}0, {}\n".format(storeOp, reg, register)

	def generateArrayDeclaration(self, current_ast_node, declarationType=""):
		arrayName = current_ast_node.value
		arraySize = -1
		arrayGlobalName = "{}.{}".format(self.currentFunction, arrayName)
		arrayGlobalReg = "{}($gp)".format(self.globalStackCounter)

		if declarationType == "global":
			arrayGlobalName = "global.{}".format(arrayName)
			self.globalstring += "\n\tla $t0, {}\n".format(arrayGlobalName)
			self.globalstring += "\tsw $t0, {}\n".format(arrayGlobalReg)
			self.incrementGlobalStackCounter()

		# Just declarating the array
		if len(current_ast_node.children) == 1:
			arraySize = current_ast_node.getChild(0).value
			self.current_symboltable.registerDict[arrayName] = arrayGlobalName 
			self.datastring += "{}: .word 0:{}\n".format(arrayGlobalName, arraySize)

		# Declaration and definition
		else:
			loopIndex = 0
			if current_ast_node.getChild(0).name == "array length":
				arraySize = int(current_ast_node.getChild(0).value)
				loopIndex = 1
			else:
				arraySize = len(current_ast_node.children)
			
			arrayElements = [0 for x in range(arraySize)]

			for i in range(loopIndex, len(current_ast_node.children)):
				if i - loopIndex >= len(arrayElements):
					break

				value = ""
				if current_ast_node.type == "char*" or current_ast_node.type == "float":
					value = current_ast_node.getChild(i).value
				else:
					value = self.generateExpression(current_ast_node.getChild(i))[0]
				arrayElements[i - loopIndex] = value

			# If array consists of strings
			if current_ast_node.type == "char*":
				self.datastring += "{}: .word 0:{}\n".format(arrayGlobalName, arraySize)

				self.textstring += "\tla $t1, {}\n".format(arrayGlobalName)
				for x in range(len(arrayElements)):
					stringName = self.generateStringConst(self.currentFunction, arrayElements[x])[0]
					self.textstring += "\tla $t0, {}\n".format(stringName)
					self.textstring += "\tsw $t0, {}($t1)\n".format(x * 4)

			# If array consists of any other type
			else:
				declType = "word"
				if current_ast_node.type == "float":
					declType = "float"
				inputName = "{}.{}".format(self.currentFunction, arrayName)
				if declarationType == "global":
					inputName = arrayGlobalName

				self.datastring += "{}: .{} {}\n".format(inputName, declType, ", ".join(arrayElements))

		if declarationType == "global":
			self.current_symboltable.registerDict[arrayName] = arrayGlobalReg
		else:
			self.current_symboltable.registerDict[arrayName] = arrayGlobalName

		self.current_symboltable.symbolLength[arrayName] = arraySize		

	def generateArithmetic(self, current_ast_node, resultReg="0"):
		arC = self.arithmeticChild

		instructions = {
						"+": "add",
						"-": "sub",
						"*": "mult",
						"/": "div"
		}

		finalReg = {
					"left": 0,
					"right": 2
		}

		operand = current_ast_node.name
		outputReg = ""

		leftChild = current_ast_node.getChild(0)
		rightChild = current_ast_node.getChild(1)
		
		self.arithmeticChild = "left"
		leftReg, leftVarType, leftType = self.generateExpression(leftChild)

		if leftReg == "$v1":
			leftReg = "{}($sp)".format(self.functionDict[self.currentFunction])
			leftVarType = "identifier"
			self.textstring += "\tsw $v1, {}\n".format(leftReg)
			self.incrementFunctionStackCounter()
		elif leftReg == "$f12":
			leftReg = "{}($sp)".format(self.functionDict[self.currentFunction])
			leftVarType = "identifier"
			self.textstring += "\ts.s $f12, {}\n".format(leftReg)
			self.incrementFunctionStackCounter()

		self.arithmeticChild = "right"
		rightReg, rightVarType, rightType = self.generateExpression(rightChild)
		self.arithmeticChild = "left"

		instr = instructions[current_ast_node.name]

		if arC == "left":
			leftReg, leftType, leftVarType, rightReg, rightType, rightVarType = self.generateTypeCast(leftReg, leftType, leftVarType,
																				rightReg, rightType, rightVarType, "0", "1")
		elif arC == "right":
			leftReg, leftType, leftVarType, rightReg, rightType, rightVarType = self.generateTypeCast(leftReg, leftType, leftVarType,
																				rightReg, rightType, rightVarType, "2", "3")

		returnType = "float"
		if leftType != "float" and rightType != "float":
			returnType = "int"	

		reg = "t"
		if leftType == "float":
			reg = "f"
			if instr == "mult":
				instr = instr[:-1]
			instr += ".s"

		if rightVarType == "const" and leftVarType == "const":
			ops = 	{
						"+": operator.add,
						"-": operator.sub,
						"*": operator.mul,
						"/": operator.truediv
					}

			outputReg = str(int(ops[operand](float(leftReg), float(rightReg))))

			return outputReg, "const", returnType

		if leftVarType != "const" and rightVarType == "const" and (instr == "add" or instr == "sub"):
			if arC == "left":
				leftReg = self.loadIntoRegister(reg, "0", leftReg)
			else:
				leftReg = self.loadIntoRegister(reg, "2", leftReg)
				
			if operand == "-" and rightReg[0] == "-":
				rightReg = rightReg[1:]			
			elif operand == "-" and rightReg[0] != "-":
				rightReg = "-" + rightReg

			resultReg = "${}{}".format(reg, finalReg[arC])

			self.textstring += "\taddi {}, {}, {}\n".format(resultReg, leftReg, rightReg)

			return resultReg, "register", returnType

		if rightVarType == "const":
			tempReg = "${}{}".format(reg, str(finalReg[arC] + 1))
			self.textstring += "\tli {}, {}\n".format(tempReg, rightReg)
			rightReg = tempReg
		elif rightVarType == "identifier":
			rightReg = self.loadIntoRegister(reg, str(finalReg[arC] + 1), rightReg)
		elif rightVarType == "data":
			rightReg = self.loadIntoRegister(reg, str(finalReg[arC] + 1), rightReg, True)
		elif rightVarType == "register":
			rightLoadReg = "${}{}".format(reg, str(finalReg[arC] + 1))
			if rightReg != rightLoadReg:
				pass
			else:
				if reg == "f":
					self.textstring += "\tmov.s {}, {}\n".format(rightLoadReg, rightReg)
				else:
					self.textstring += "\tmove {}, {}\n".format(rightLoadReg, rightReg)
				rightReg = rightLoadReg

		if leftVarType == "const":
			tempReg = "${}{}".format(reg, str(finalReg[arC]))
			self.textstring += "\tli {}, {}\n".format(tempReg, leftReg)
			leftReg = tempReg
		elif leftVarType == "identifier":
			leftReg = self.loadIntoRegister(reg, str(finalReg[arC]), leftReg)
		elif leftVarType == "data":
			leftReg = self.loadIntoRegister(reg, str(finalReg[arC]), leftReg, True)
		elif leftVarType == "register":
			leftLoadReg = "${}{}".format(reg, str(finalReg[arC]))
			if leftReg != leftLoadReg:
				pass
			else:
				if reg == "f":
					self.textstring += "\tmov.s {}, {}\n".format(leftLoadReg, leftReg)
				else:
					self.textstring += "\tmove {}, {}\n".format(leftLoadReg, leftReg)
				leftReg = leftLoadReg

		resultReg = "${}{}".format(reg, str(finalReg[arC]))

		if instr in ["mult", "div"]:
				self.textstring += "\t{} {}, {}\n".format(instr, leftReg, rightReg)
				self.textstring += "\tmflo {}\n".format(resultReg)
		else:
			if current_ast_node.parent.name not in ["+", "-", "*", "/"]:
				self.textstring += "\t{} {}, {}, {}\n".format(instr, resultReg, leftReg, rightReg)
				return resultReg, "register", returnType			
			else:
				self.textstring += "\t{} {}, {}, {}\n".format(instr, resultReg, leftReg, rightReg)

		return resultReg, "register", returnType

	def generateCondition(self, current_ast_node):
		comp_operators = {
			"==": "seq",
			"!=": "sne",
			">": "sgt",
			">=": "sge",
			"<": "slt",
			"<=": "sle"
		}

		operator = comp_operators[current_ast_node.name]

		leftReg, leftVarType, leftType = self.generateExpression(current_ast_node.getChild(0))
		self.arithmeticChild = "right"
		rightReg, rightVarType, rightType = self.generateExpression(current_ast_node.getChild(1))

		leftReg, leftType, leftVarType, rightReg, rightType, rightVarType = self.generateTypeCast(leftReg, leftType, leftVarType,
																				rightReg, rightType, rightVarType, "0", "1")

		reg = "t"
		if leftType == "float":
			reg = "f"
			if operator not in ["sgt", "sge"]:
				operator = "c." + operator[1:] + ".s"
			elif operator == "sgt" or operator == "sge":
				tempReg, tempVarType, tempType = leftReg, leftVarType, leftType
				leftReg, leftVarType, leftType = rightReg, rightVarType, rightType
				rightReg, rightVarType, rightType = tempReg, tempVarType, tempType

				operator = "c.lt.s"
				if operator == "sge":
					operator = "c.le.s"			

		if leftVarType == "const":
			self.textstring += "\tli ${}0, {}\n".format(reg, leftReg)
			leftReg = "${}0".format(reg)
		elif leftVarType == "identifier" or leftVarType == "data":
			self.textstring += "\tlw ${}0, {}\n".format(reg, leftReg)
			leftReg = "${}0".format(reg)

		if rightVarType == "const":
			self.textstring += "\tli ${}1, {}\n".format(reg, rightReg)
			rightReg = "${}1".format(reg)
		elif rightVarType == "identifier" or rightVarType == "data":
			self.textstring += "\tlw ${}1, {}\n".format(reg, rightReg)
			rightReg = "${}1".format(reg)

		if leftType == "float":
			self.textstring += "\t{} {}, {}\n".format(operator, leftReg, rightReg)
		else:
			self.textstring += "\t{} $t0, {}, {}\n".format(operator, leftReg, rightReg)

		returnType = "int"
		if reg == "f":
			returnType = "float"

		return "${}0".format(reg), "register", returnType

	def generateFunctionCall(self, current_ast_node):
		totalArguments = self.current_symboltable.getSymbolLength(current_ast_node.value)
		
		if totalArguments != len(current_ast_node.children):
			raise Exception("\033[91mTotal input arguments on {} should be {}\033[0m".format(current_ast_node.value, totalArguments))
		
		if totalArguments != 0:
			self.textstring += "\taddiu $sp, $sp, -{}\n".format(str(totalArguments * 4))

		tempString = self.textstring
		self.textstring = ""

		for i in range(totalArguments):
			result, resultType, regType = self.generateExpression(current_ast_node.getChild(i))

			reg = "t"
			if current_ast_node.getChild(i).type == "float":
					reg = "f"

			resultReg = "${}0".format(reg)
			if resultType == "const":
				self.textstring += "\tli {}, {}\n".format(resultReg, result)

			elif resultType == "data":
				self.textstring += "\tla {}, {}\n".format(resultReg, result)

			elif resultType == "identifier":
				try:
					tempIndex = result[:-5]
					result = str(int(tempIndex) + (totalArguments * 4)) + "($sp)"
					self.textstring += "\tlw {}, {}\n".format(resultReg, result)
				except ValueError:
					self.textstring += "\tlw {}, {}\n".format(resultReg, result)

					ph_registers = set(re.findall(f"{self.currentFunction}\.ph\.", self.textstring))
					for ph in ph_registers:
						self.textstring = self.textstring.replace(ph, f'{ph.replace("ph", "aph")}{totalArguments * 4}.')

			elif resultType == "register":
				# this is some real hacky stuff but it's 3am and I want to sleep
				# looks for variables that were put on the stack by generateExpression
				# then replaces their placeholders with an alternative (aph) that contains the extra offset needed to be added
				ph_registers = set(re.findall(f"{self.currentFunction}\.ph\.", self.textstring))
				for ph in ph_registers:
					self.textstring = self.textstring.replace(ph, f'{ph.replace("ph", "aph")}{totalArguments * 4}.')

				resultReg = result

			self.textstring += "\tsw {}, {}($sp)\n".format(resultReg, i * 4)

		self.textstring += "\tjal {}\n".format(current_ast_node.value)
		self.textstring += "\taddiu $sp, $sp, {}\n".format(totalArguments * 4)

		self.textstring = tempString + self.textstring

		if self.current_symboltable.getSymbolType(current_ast_node.value) == "float":
			return "$f12", "register", "float"
		else:
			return "$v1", "register", "int"

	def eliminateUselessBranch(self, newLabel):
		# using \n here instead of $ because it doesn't seem to work
		match = re.findall(r"L[0-9]+:$\n\Z", self.textstring)
		if len(match) != 0:
			match = match[0]
			label = re.findall(r"L[0-9]+", match)[0]
			self.textstring = self.textstring[:-len(match)]
			self.textstring = self.textstring.replace(label, newLabel)

	def generateIfStatement(self, current_ast_node):
		thirdChild = len(current_ast_node.children) == 3

		# generate the condition check
		firstLabel = self.getNewLabel()
		condReg, condVarType, condType = self.generateExpression(current_ast_node.getChild(0))
		if condType == "float":
			self.textstring += "\tbc1f {}\n".format(firstLabel)
		else:
			self.textstring += "\tbeq $zero, {}, {}\n\n".format(condReg, firstLabel)

		# generate the first codeblock
		self.generateCodeBlock(current_ast_node.getChild(1))
		if thirdChild:
			placeholderLabel = "%.placeholder.{}".format(self.currentDepth)
			self.eliminateUselessBranch(placeholderLabel)
			self.textstring += "\tb {}\n\n".format(placeholderLabel)
		else:
			self.textstring = self.textstring.replace("%.placeholder.{}".format(self.currentDepth), firstLabel)
		self.textstring += "{}:\n".format(firstLabel)

		# generate else, else if, while
		if thirdChild:
			lastChild = current_ast_node.getChild(2)
			if lastChild.name == "code block":
				self.generateCodeBlock(lastChild)
				exitLabel = self.getNewLabel()
				self.textstring = self.textstring.replace("%.placeholder.{}".format(self.currentDepth), exitLabel)
				self.textstring += "{}:\n".format(exitLabel)
			elif lastChild.name == "if":
				self.generateIfStatement(lastChild)
			elif lastChild.name == "while":
				self.generateWhileStatement(lastChild, firstLabel)
				exitLabel = self.getNewLabel()
				self.textstring += "{}:\n".format(exitLabel)
				self.textstring = self.textstring.replace("%.placeholder.{}".format(self.currentDepth), exitLabel)

	def generateWhileStatement(self, current_ast_node, ifLabel=None):
		blockLabel = ""
		if not ifLabel: 
			blockLabel = self.getNewLabel()
		else:
			blockLabel = ifLabel
		checkLabel = self.getNewLabel()

		# if the while is located in an if, the jump whill already be written by the if
		if not ifLabel:
			# jump to the check label
			self.eliminateUselessBranch(checkLabel)
			self.textstring += "\tb {}\n\n".format(checkLabel)
			
			# block label
			self.textstring += "{}:\n".format(blockLabel)

		# generate the code block
		self.generateCodeBlock(current_ast_node.getChild(1))

		temp_table = self.current_symboltable
		self.current_symboltable = self.current_symboltable.children[self.current_symboltable.childIndex - 1]
		# generate the check block
		self.textstring += "{}:\n".format(checkLabel)
		condReg, condVarType, condType = self.generateExpression(current_ast_node.getChild(0))
		if condType == "float":
			self.textstring += "\tbc1t {}\n".format(blockLabel)
		else:
			self.textstring += "\tbne $zero, {}, {}\n\n".format(condReg, blockLabel)

		self.current_symboltable = temp_table

	def printHelperFunction(self, current_ast_node, arg):
		syscall = {"%d": 1, "%f": 2, "%s": 4, "%c": 11}

		self.textstring += "\tli $v0, {}\n".format(syscall[arg])

		result, varType, regType = self.generateExpression(current_ast_node)
		if varType == "data":
			if arg == "%f":
				result = self.loadIntoRegister("f", 0, result)
				self.textstring += "\tmov.s $f12, {}\n".format(result)
			elif arg == "%s":
				result = self.loadIntoRegister("t", 0, result, True)
				self.textstring += "\tmove $a0, {}\n".format(result)

		elif varType == "identifier":
			loadType = self.current_symboltable.getSymbolType(current_ast_node.value)
			if loadType == "float":
				self.textstring += "\tl.s $f12, {}\n".format(result)
			elif loadType == "char*":
				self.textstring += "\tlw $t0, {}\n".format(result)
				self.textstring += "\tmove $a0, $t0\n"
			else:
				self.textstring += "\tlw $a0, {}\n".format(result)

		elif varType == "register":
			if result[1] == "f":
				self.textstring += "\tmov.s $f12, {}\n".format(result)
			elif result[1] == "t":
				self.textstring += "\tmove $a0, {}\n".format(result)
			elif result[1] == "v":
				self.textstring += "\tmove $a0, {}\n".format(result)

		else:
			self.textstring += "\tli $a0, {}\n".format(result)
			
		self.textstring += "\tsyscall\n\n"

	def generatePrint(self, current_ast_node):
		firstArg = current_ast_node.getChild(0)
		if firstArg.name == "identifier" or firstArg.name == "f call":
			argTypes = {"int": "%d", "float": "%f", "char*": "%s", "char": "%c"}
			self.printHelperFunction(firstArg, argTypes[self.current_symboltable.getSymbolType(firstArg.value)])
			return

		printString = current_ast_node.getChild(0).value
		# all argument strings
		args = [arg for arg in re.findall("%[sfdc]", printString)]
		# all non-argument strings
		nonArgs = re.split("%[sfdc]", printString.strip('"'))

		try:
			for i in range(len(nonArgs)):
				# print the normal string const
				nonArg = nonArgs[i]
				if len(nonArg) != 0:
					self.textstring += "\tli $v0, 4\n"
					string = self.generateStringConst(self.currentFunction, '"{}"'.format(nonArg))[0]
					result = self.loadIntoRegister("t", 0, string, True)
					self.textstring += "\tmove $a0, {}\n".format(result)
					self.textstring += "\tsyscall\n\n"

				# fill in the argument
				if i < len(args):
					self.printHelperFunction(current_ast_node.getChild(1 + i), args[i])
		except IndexError:
			# raise an exception if there is an insufficient amount of arguments for the printf functionDict
			raise Exception("\033[91min printf({}): {} {} arguments, got {}\033[0m".format(printString, "expected", len(args), len(current_ast_node.children) - 1))

	def generateScan(self, current_ast_node):
		syscall = {"%d": 5, "%f": 6, "%s": 8, "%c": 12}

		if len(current_ast_node.children) != 2:
			raise Exception("\033[91m'scanf' expected 2 arguments, got {}\033[0m".format(len(current_ast_node.children)))
		inputString = current_ast_node.getChild(0).value.strip('"')
		self.textstring += "\tli $v0, {}\n".format(syscall[inputString])
		self.textstring += "\tsyscall\n"

		rightChild = current_ast_node.getChild(1)
		result, varType, regType = self.generateExpression(rightChild)

		if self.current_symboltable.getSymbolType(rightChild.value) == "float":
			if varType == "identifier":
				self.textstring += "\ts.s $f0, {}\n".format(result)
			elif rightChild.name == "array address" or rightChild.name == "address":
				self.textstring += "\ts.s $f0, ({})\n".format(result)
			elif varType == "register":
				self.textstring += "\tmov.s $f0, {}\n".format(result)
		else:
			if varType == "identifier":
				self.textstring += "\tsw $v0, {}\n".format(result)
			elif rightChild.name == "array address" or rightChild.name == "address":
				self.textstring += "\tsw $v0, ({})\n".format(result)
			elif varType == "register":
				self.textstring += "\tmove {}, $v0\n".format(result)

	def generateReturn(self, current_ast_node):
		returnChild = current_ast_node.getChild(0)
		result, resultType, regType = self.generateExpression(returnChild)

		if resultType == "identifier":
			if self.current_symboltable.getSymbolType(self.currentFunction) == "float":
				self.textstring += "\tl.s $f12, {}\n".format(result)
			elif self.current_symboltable.getSymbolType(self.currentFunction) == "char*":
				self.textstring += "\tla $v1, {}\n".format(result)
			else:
				self.textstring += "\tlw $v1, {}\n".format(result)

		elif resultType == "register" or resultType == "data":
			if self.current_symboltable.getSymbolType(self.currentFunction) == "float":
				self.textstring += "\tmov.s $f12, {}\n".format(result)
			else:
				self.textstring += "\tmove $v1, {}\n".format(result)

		else:
			self.textstring += "\tli $v1, {}\n".format(result)

		self.textstring += "\tb {}.exit\n".format(self.currentFunction)
