# CS 4308
# Group Members:Sam Perez
# This is our Interpreter program and it translates the tokens found by the scanner and organized by the parser
# In other words it converts the tokens into executable instructions in the IDE
#
# This interpreter is incomplete and does not correctly provide the target output. However, concepts in this code 
# are correct and can be utilized for conceptual knowledge, not implementation
# The correct output for the interpretor are provided in a word document and the psuedocode for this interpretor are 
# also provided in a separate word document. 
#
# The file used to test this interpeter is test.scl


# Import all files created for the interpretor, scanner, node, and parser
from scanner import *
from node import *
from parser import *

class Interpreter(Parser):
    # Constructor
    def __init__(self, sclFilePath):
        #Parser.__init__(self, sclFilePath)
        self.vars = {}
        self.cons = {}
        self.var_input = {}
        self.cons_input = {}

    # Performs Python-SCL Interpretation
    def interpret(self, filePath):
        print("Parsing SCL File", "\n")
        parser = Parser()
        parseTree = parser.fileTime(filePath)
        print("\nFinished Parsing SCL File")
        print("="*50, "\n")

        # Run through all the node's direct children
        for node in parseTree.getChildren():
            if node.getType() is NodeType.IMPORT:
                pass
            elif node.getType() is NodeType.SYMBOL:
                pass
            elif node.getType() is NodeType.GLOBALS:
                self.interpretGlobals(node)
            elif node.getType() is NodeType.IMPLEMENT:
                self.interpretImplement(node)

    # Interprets globals
    def interpretGlobals(self, node):
        for child in node.getChildren():
            if child.getType() is NodeType.CONST_DEC:
                self.interpretConstDec(child)
            elif child.getType() is NodeType.IDENTIFIER:
                self.interpretIdentifer(child)

    # Interprets implement
    def interpretImplement(self, node):
        if node.getChildren() == None:
            return
        for child in node.getChildren():
            if child.getType() is NodeType.KEYWORDS:
                self.interpretKeywords(child)

    # Interprets const_dec
    def interpretConstDec(self, node):
        # There should only be one child of <const_dec>
        for child in node.getChildren():
            if child.getType() is NodeType.CONST_LIST:
                self.interpretConstList(child)

    # Interprets const_list
    def interpretConstList(self, node):
        for child in node.getChildren():
            if child.getType() is NodeType.COMP_DECLARE:
                self.interpretCompDeclare(child)

    # Interprets indentifier
    def interpretIdentifer(self, node):
        # There should only be one child of <identifier>
        for child in node.getChildren():
            if child.getType() is NodeType.VAR_LIST:
                self.interpretVarList(child)

    # Interprets var_list
    def interpretVarList(self, node):
        for child in node.getChildren():
            if child.getType() is NodeType.COMP_DECLARE:
                self.interpretCompDeclare(child)

    # Interprets comp_declare
    def interpretCompDeclare(self, node):
        parent = node.getParent()
        greatGrandparent = parent.getParent().getParent()

        isConstant = True if parent.getType() is NodeType.CONST_LIST else False
        isGlobal = True if greatGrandparent.getType() is NodeType.GLOBALS else False

        lexemes = node.getScanLine().getLexemes()
        token_type = None

        for child in node.getChildren():
            if child.getType() is NodeType.RET_TYPE:
                token_type = self.interpretRetType(child)

        if isGlobal is True:
            if isConstant is True:
                self.cons[lexemes[1].getLexemeString()] = [
                    lexemes[3].getLexemeString(), token_type]
            else:
                self.vars[lexemes[1].getLexemeString()] = [
                    "", token_type]
        else:
            if isConstant is True:
                self.cons_input[lexemes[1].getLexemeString()] = [
                    lexemes[3].getLexemeString(), token_type]
            else:
                self.var_input[lexemes[1].getLexemeString()] = [
                    "", token_type]

    # Returns return type token
    def interpretRetType(self, node):
        lexemes = node.getScanLine().getLexemes()

        returnType = lexemes[len(lexemes)-1]
        token_type = returnType.getToken()

        return token_type

    # Interprets Keywords
    def interpretKeywords(self, node):
        if node.getChildren() == None:
            return
        for child in node.getChildren():
            if child.getType() is NodeType.OPERATORS:
                self.interpretOperators(child)

    # Interprets operators
    def interpretOperators(self, node):
        if node.getChildren() == None:
            return
        for child in node.getChildren():
            if child.getType() is NodeType.CONST_DEC:
                self.interpretConstDec(child)
            elif child.getType() is NodeType.IDENTIFIER:
                self.interpretIdentifer(child)
            elif child.getType() is NodeType.PACTIONS:
                self.interpretPActions(child)

    # Interprets pactions
    def interpretPActions(self, node):
        for child in node.getChildren():
            if child.getType() is NodeType.ACTION_DEF:
                self.interpretActionDef(child)

    # Interprets action_def
    def interpretActionDef(self, node):
        lexemes = node.getScanLine().getLexemes()

        # If action is to SET
        if lexemes[0].getToken() is Token.SET:
            if lexemes[1].getLexemeString() in self.vars:
                expResult = None
                for child in node.getChildren():
                    if child.getType() is NodeType.EXP:
                        expResult = self.interpretExp(child)
                        self.vars[lexemes[1].getLexemeString(
                        )][0] = expResult
            elif lexemes[1].getLexemeString() in self.var_input:
                expResult = None
                for child in node.getChildren():
                    if child.getType() is NodeType.EXP:
                        expResult = self.interpretExp(child)
                        self.var_input[lexemes[1].getLexemeString(
                        )][0] = expResult
            elif lexemes[1].getLexemeString() in (self.cons, self.cons_input):
                print("ERROR: Constant variable cannot be changed!")
            else:
                print("ERROR: Variable not found!")

        # If action is to INPUT
        elif lexemes[0].getToken() is Token.INPUT:
            if lexemes[1].getToken() is Token.STRING_LITERAL:
                if self.getVarType(lexemes[2].getLexemeString()) is not None:
                    if lexemes[2].getLexemeString() in self.vars:
                        self.vars[lexemes[2].getLexemeString()][0] = input(
                            self.getLiteralString(lexemes[1].getLexemeString()))
                    elif lexemes[2].getLexemeString() in self.var_input:
                        self.var_input[lexemes[2].getLexemeString()][0] = input(
                            self.getLiteralString(lexemes[1].getLexemeString()))
                    elif lexemes[2].getLexemeString() in (self.cons, self.cons_input):
                        print("ERROR: Constant Variable cannot be changed!")
                    else:
                        print("ERROR: Variable not found!")

        # If action is to DISPLAY
        elif lexemes[0].getToken() is Token.DISPLAY:
            # Should only be one child
            for child in node.getChildren():
                valueListTxt = self.interpretPVarValueList((child))
                print(valueListTxt)

    # Interprets p_var_value_list and returns a list of values
    def interpretPVarValueList(self, node):
        allLexemesOnLine = node.getScanLine().getLexemes()

        valueListLexemes = allLexemesOnLine[1:len(allLexemesOnLine)]
        printString = ""

        for lexeme in valueListLexemes:
            # Compares if token is not a string literal 
            if lexeme.getToken().getNumCode() in (2, 3, 5, 6, 7, 9):
                printString += str(self.getVarValue(lexeme.getLexemeString()))
            # Compares if it is string ident or const string ident 
            elif lexeme.getToken().getNumCode() in (4, 8):
                printString += str(self.getLiteralString(
                    self.getVarValue(lexeme.getLexemeString())))
            # Compares if a token is not a string literal
            elif lexeme.getToken().getNumCode() in (10, 11, 13):
                printString += str(lexeme.getLexemeString())
            # Compares if a token is a string literal
            elif lexeme.getToken() is Token.STRING_LITERAL:
                printString += str(self.getLiteralString(lexeme.getLexemeString()))

        return printString

    # Returns string value which excludes the quotes and comma
    def getLiteralString(self, lexemeStr):
        result = re.search("\"(.*)\"", lexemeStr)
        return result.group(1)

    # Interprets exp node and returns expression value
    def interpretExp(self, node):
        allLexemesOnLine = node.getScanLine().getLexemes()

        expLexemes = allLexemesOnLine[3:len(allLexemesOnLine)]

        # Create a precedence for operands
        precedence = {"*": 1, "/": 1, "+": 2, "-": 2}

        lexemeList = []
        operList = []

        index = 0
        exprResult = 0

        for lexeme in expLexemes:
            if lexeme.getToken().getNumCode() in (2, 3, 6, 7, 10, 11):
                lexemeList.append(lexeme)
            elif lexeme.getToken().getNumCode() in (25, 26, 27, 28):
                while len(operList) != 0 and precedence[operList[len(operList)-1]] <= precedence[lexeme.getLexemeString()]:
                    lexemeList.append(
                        Lexeme(operList[len(operList)-1], Token.findToken(operList.pop())))
                operList.append(lexeme.getLexemeString())

        while len(operList) != 0:
            lexemeList.append(
                Lexeme(operList[len(operList) - 1], Token.findToken(operList.pop())))

        postFixList = []

        for lexeme in lexemeList:
            if lexeme.getToken() is Token.MUL_OPERATOR:
                self.mulOper(postFixList)
            elif lexeme.getToken() is Token.DIV_OPERATOR:
                self.divOper(postFixList)
            elif lexeme.getToken() is Token.ADD_OPERATOR:
                self.addOper(postFixList)
            elif lexeme.getToken() is Token.SUB_OPERATOR:
                self.subOper(postFixList)
            else:
                postFixList.append(lexeme.getLexemeString())

        return postFixList.pop()

    # Multiplies the two top elements in postFixList
    def mulOper(self, postFixList):
        varTwo = postFixList.pop()
        varOne = postFixList.pop()

        valOne = None
        valTwo = None

        # Find value of first variable
        if Token.findToken(varOne) is Token.INTEGER_LITERAL:
            valOne = int(varOne)
        elif Token.findToken(varOne) is Token.FLOAT_LITERAL:
            valOne = float(varOne)
        else:
            varOneType = self.getVarType(varOne)
            if varOneType is Token.INTEGER:
                valOne = int(self.getVarValue(varOne))
            elif varOneType is Token.FLOAT:
                valOne = float(self.getVarValue(varOne))

        # Find value of second variable
        if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
            valTwo = int(varTwo)
        elif Token.findToken(varTwo) is Token.FLOAT_LITERAL:
            valTwo = float(varTwo)
        else:
            varTwoType = self.getVarType(varTwo)
            if varTwoType is Token.INTEGER:
                valTwo = int(self.getVarValue(varTwo))
            elif varTwoType is Token.FLOAT:
                valTwo = float(self.getVarValue(varTwo))

        result = valOne * valTwo
        postFixList.append(str(result))

    # Divides the two top elements in postFixList
    def divOper(self, postFixList):
        varTwo = postFixList.pop()
        varOne = postFixList.pop()

        valOne = None
        valTwo = None

        # Find value of first variable
        if Token.findToken(varOne) is Token.INTEGER_LITERAL:
            valOne = int(varOne)
        elif Token.findToken(varOne) is Token.FLOAT_LITERAL:
            valOne = float(varOne)
        else:
            varOneType = self.getVarType(varOne)
            if varOneType is Token.INTEGER:
                valOne = int(self.getVarValue(varOne))
            elif varOneType is Token.FLOAT:
                valOne = float(self.getVarValue(varOne))

        # Find value of second variable
        if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
            valTwo = int(varTwo)
        elif Token.findToken(varTwo) is Token.FLOAT_LITERAL:
            valTwo = float(varTwo)
        else:
            varTwoType = self.getVarType(varTwo)
            if varTwoType is Token.INTEGER:
                valTwo = int(self.getVarValue(varTwo))
            elif varTwoType is Token.FLOAT:
                valTwo = float(self.getVarValue(varTwo))

        result = valOne / valTwo
        postFixList.append(str(result))

    # Adds the two top elements in postFixList
    def addOper(self, postFixList):
        varTwo = postFixList.pop()
        varOne = postFixList.pop()

        valOne = None
        valTwo = None

        # Find value of first variable
        if Token.findToken(varOne) is Token.INTEGER_LITERAL:
            valOne = int(varOne)
        elif Token.findToken(varOne) is Token.FLOAT_LITERAL:
            valOne = float(varOne)
        else:
            varOneType = self.getVarType(varOne)
            if varOneType is Token.INTEGER:
                valOne = int(self.getVarValue(varOne))
            elif varOneType is Token.FLOAT:
                valOne = float(self.getVarValue(varOne))

        # Find value of second variable
        if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
            valTwo = int(varTwo)
        elif Token.findToken(varTwo) is Token.FLOAT_LITERAL:
            valTwo = float(varTwo)
        else:
            varTwoType = self.getVarType(varTwo)
            if varTwoType is Token.INTEGER:
                valTwo = int(self.getVarValue(varTwo))
            elif varTwoType is Token.FLOAT:
                valTwo = float(self.getVarValue(varTwo))

        result = valOne + valTwo
        postFixList.append(str(result))

    # Subtracts the two top elements in postFixList
    def subOper(self, postFixList):
        varTwo = postFixList.pop()
        varOne = postFixList.pop()

        valOne = None
        valTwo = None

        # Find value of first variable
        if Token.findToken(varOne) is Token.INTEGER_LITERAL:
            valOne = int(varOne)
        elif Token.findToken(varOne) is Token.FLOAT_LITERAL:
            valOne = float(varOne)
        else:
            varOneType = self.getVarType(varOne)
            if varOneType is Token.INTEGER:
                valOne = int(self.getVarValue(varOne))
            elif varOneType is Token.FLOAT:
                valOne = float(self.getVarValue(varOne))

        # Find value of second variable
        if Token.findToken(varTwo) is Token.INTEGER_LITERAL:
            valTwo = int(varTwo)
        elif Token.findToken(varTwo) is Token.FLOAT_LITERAL:
            valTwo = float(varTwo)
        else:
            varTwoType = self.getVarType(varTwo)
            if varTwoType is Token.INTEGER:
                valTwo = int(self.getVarValue(varTwo))
            elif varTwoType is Token.FLOAT:
                valTwo = float(self.getVarValue(varTwo))

        result = valOne * valTwo
        postFixList.append(str(result))

    # Looks up the stored value of the variable identity lexeme
    def getVarValue(self, varIdent):
        varVal = None

        if str(varIdent) in self.vars:
            varVal = self.vars[str(varIdent)][0]
        elif str(varIdent) in self.cons:
            varVal = self.cons[str(varIdent)][0]
        elif str(varIdent) in self.var_input:
            varVal = self.var_input[str(varIdent)][0]
        elif str(varIdent) in self.cons_input:
            varVal = self.cons_input[str(varIdent)][0]

        return varVal

    # Looks up the stored type of the variable identity lexeme
    def getVarType(self, varIdent):
        varType = None

        if str(varIdent) in self.vars:
            varType = self.vars[str(varIdent)][1]
        elif str(varIdent) in self.cons:
            varType = self.cons[str(varIdent)][1]
        elif str(varIdent) in self.var_input:
            varType = self.var_input[str(varIdent)][1]
        elif str(varIdent) in self.cons_input:
            varType = self.cons_input[str(varIdent)][1]

        return varType

    # If the lexeme is a number, true 
    def isNumber(self, varIdent):
        varType = self.getVarType(varIdent)

        if varType is Token.INTEGER or varType is Token.FLOAT:
            return True
        else:
            return False


# Method/Class to get input for the file
txtFile = input("Type in a file(insert quotation marks around the file): ")

# The file is only sent to the parser method if it is not empty
# This does not take nonexistance of a file into consideration
if (txtFile == ""):
    print("Empty Input, Please input a valid file.")
else:
    parser = Parser()
    interp = Interpreter(parser)
    interp.interpret(txtFile)
