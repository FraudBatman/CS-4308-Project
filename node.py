from enum import Enum

class Node:

	# Constructor
	def __init__(self, parent, scanLine, Type):
		self.parent = parent
		self.children = None
		self.scanLine = scanLine
		self.Type = Type

	# Getter Methods for all fields
	def getParent(self):
		return self.parent

	def getChildren(self):
		return self.children

	def getScanLine(self):
		return self.scanLine

	def getType(self):
		return self.Type

	# Setter Methods for all fields
	def setParent(self, parent):
		self.parent = parent

	def setChildren(self, children):
		self.children = children

	def setScanLine(self, scanLine):
		self.scanLine = scanLine

	def setType(self, Type):
		self.Type = Type

	# Adds node object to children list
	def add_c_node(self, child):
		if self.children is None:
			self.children = []  # Convert to array from None type

		self.children.append(child)

	# Removes node object from children list
	def remove_c_node(self, child):
		if self.children is not None:
			self.children.remove(child)
			child.setParent(None)

	# Returns the distance from the root node
	def getDepth(self):
		if self.getParent() is None:
			return 0
		else:
			currentNode = self
			depth = 0
			while currentNode.getParent() is not None:
				depth += 1
				currentNode = currentNode.getParent()
			return depth



class Type(Enum):

	PROGRAM = "<program>"
	IMPORT = "<import_stmnt>"
	SYMBOL = "<symbol_stmnt>"
	GLOBALS = "<globals>"
	IMPLEMENT = "<implement>"
	CONST_DEC = "<const_dec>"
	CONST_LIST = "<const_list>"
	IDENTIFIER = "<identifier>"
	VAR_LIST = "<var_list>"
	COMP_DECLARE = "<comp_declare>"
	RET_TYPE = "<ret_type>"
	KEYWORDS = "<keywords>"
	OPERATORS = "<operators>"
	PACTIONS = "<pactions>"
	ACTION_DEF = "<action_def>"
	EXP = "<exp>"
	PVAR_LIST = "<p_var_list>"