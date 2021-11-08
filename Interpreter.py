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

        # Switch statement to run through all the node's direct children
        for node in parseTree.getChildren():
            if node.getType() is Type.IMPORT:
                pass
            elif node.getType() is Type.SYMBOL:
                pass
            elif node.getType() is Type.GLOBALS:
                self.interp_default(node)
            elif node.getType() is Type.IMPLEMENT:
                self.interp_imp(node)



    # The following methods interpret tokens
    # default tokens
    def interp_default(self, node):
        for child in node.getChildren():
            if child.getType() is Type.CONST_DEC:
                self.interp_const_declaration(child)
            elif child.getType() is Type.IDENTIFIER:
                self.interp_ident(child)

    # implementation
    def interp_imp(self, node):
        if node.getChildren() == None:
            return
        for child in node.getChildren():
            if child.getType() is Type.KEYWORDS:
                self.interp_keys(child)

    # constant declarations
    def interp_const_declaration(self, node):
        # There should only be one child of <const_dec>
        for child in node.getChildren():
            if child.getType() is Type.CONST_LIST:
                self.interp_c_list(child)

    # constants 
    def interp_c_list(self, node):
        for child in node.getChildren():
            if child.getType() is Type.COMP_DECLARE:
                self.interp_comp_dec(child)

    # indentifier
    def interp_ident(self, node):
        # There should only be one child of <identifier>
        for child in node.getChildren():
            if child.getType() is Type.VAR_LIST:
                self.interpretVarList(child)

    # variable list
    def interpretVarList(self, node):
        for child in node.getChildren():
            if child.getType() is Type.COMP_DECLARE:
                self.interp_comp_dec(child)

    # complete declarations
    def interp_comp_dec(self, node):
        parent = node.getParent()
        third_parent = parent.getParent().getParent()

        isConstant = True if parent.getType() is Type.CONST_LIST else False
        isDefault = True if third_parent.getType() is Type.GLOBALS else False

        lex = node.getScanLine().getLex()
        token_type = None

        for child in node.getChildren():
            if child.getType() is Type.RET_TYPE:
                token_type = self.interp_return(child)

        if isDefault is True:
            if isConstant is True:
                self.cons[lex[1].getLexStr()] = [
                    lex[3].getLexStr(), token_type]
            else:
                self.vars[lex[1].getLexStr()] = [
                    "", token_type]
        else:
            if isConstant is True:
                self.cons_input[lex[1].getLexStr()] = [
                    lex[3].getLexStr(), token_type]
            else:
                self.var_input[lex[1].getLexStr()] = [
                    "", token_type]
    #End of interpretation methods 


    # Returns return type token
    def interp_return(self, node):
        lex = node.getScanLine().getLex()

        returnType = lex[len(lex)-1]
        token_type = returnType.getToken()

        return token_type

    # Interprets Keywords
    def interp_keys(self, node):
        if node.getChildren() == None:
            return
        for child in node.getChildren():
            if child.getType() is Type.OPERATORS:
                self.interp_ops(child)

    # Interprets operators
    def interp_ops(self, node):
        if node.getChildren() == None:
            return
        for child in node.getChildren():
            if child.getType() is Type.CONST_DEC:
                self.interp_const_declaration(child)
            elif child.getType() is Type.IDENTIFIER:
                self.interp_ident(child)
            elif child.getType() is Type.PACTIONS:
                self.interpretPActions(child)

    # Interprets pactions
    def interpretPActions(self, node):
        for child in node.getChildren():
            if child.getType() is Type.ACTION_DEF:
                self.interpretActionDef(child)

    # Interprets action_def
    def interpretActionDef(self, node):
        lex = node.getScanLine().getLex()

        # If action is to SET
        if lex[0].getToken() is Token.SET:
            if lex[1].getLexStr() in self.vars:
                expr_result = None
                for child in node.getChildren():
                    if child.getType() is Type.EXP:
                        expr_result = self.interp_exprs(child)
                        self.vars[lex[1].getLexStr(
                        )][0] = expr_result
            elif lex[1].getLexStr() in self.var_input:
                expr_result = None
                for child in node.getChildren():
                    if child.getType() is Type.EXP:
                        expr_result = self.interp_exprs(child)
                        self.var_input[lex[1].getLexStr(
                        )][0] = expr_result
            elif lex[1].getLexStr() in (self.cons, self.cons_input):
                print("Cannot change constant variables.")
            else:
                print("Variable does not exist.")

        # If action is to INPUT
        elif lex[0].getToken() is Token.INPUT:
            if lex[1].getToken() is Token.STRING_LITERAL:
                if self.getVarType(lex[2].getLexStr()) is not None:
                    if lex[2].getLexStr() in self.vars:
                        self.vars[lex[2].getLexStr()][0] = input(
                            self.getLitStr(lex[1].getLexStr()))
                    elif lex[2].getLexStr() in self.var_input:
                        self.var_input[lex[2].getLexStr()][0] = input(
                            self.getLitStr(lex[1].getLexStr()))
                    elif lex[2].getLexStr() in (self.cons, self.cons_input):
                        print("Constant variables cannot be changed.")
                    else:
                        print("Variable does not exist.")

        # If action is to DISPLAY
        elif lex[0].getToken() is Token.DISPLAY:
            # Should only be one child
            for child in node.getChildren():
                valueListTxt = self.interp_pvar_list((child))
                print(valueListTxt)

    # Interprets p_var_value_list and returns a list of values
    def interp_pvar_list(self, node):
        lineLexems = node.getScanLine().getLex()

        valueListlex = lineLexems[1:len(lineLexems)]
        returnString = ""

        for lexeme in valueListlex:
            # Compares if token is not a string literal 
            if lexeme.getToken().getNumCode() in (2, 3, 5, 6, 7, 9):
                returnString += str(self.getVarValue(lexeme.getLexStr()))
            # Compares if it is string ident or const string ident 
            elif lexeme.getToken().getNumCode() in (4, 8):
                returnString += str(self.getLitStr(
                    self.getVarValue(lexeme.getLexStr())))
            # Compares if a token is not a string literal
            elif lexeme.getToken().getNumCode() in (10, 11, 13):
                returnString += str(lexeme.getLexStr())
            # Compares if a token is a string literal
            elif lexeme.getToken() is Token.STRING_LITERAL:
                returnString += str(self.getLitStr(lexeme.getLexStr()))
        return returnString

    # Returns string value which excludes the quotes and comma
    def getLitStr(self, lextr):
        result = re.search("\"(.*)\"", lextr)
        return result.group(1)

    # Interprets exp node and returns expression value
    def interp_exprs(self, node):
        lineLexems = node.getScanLine().getLex()

        explex = lineLexems[3:len(lineLexems)]

        # Create a precedence for operands
        precedence = {"*": 1, "/": 1, "+": 2, "-": 2}

        lexemeList = []
        operList = []

        index = 0
        exprResult = 0

        for lexeme in explex:
            if lexeme.getToken().getNumCode() in (2, 3, 6, 7, 10, 11):
                lexemeList.append(lexeme)
            elif lexeme.getToken().getNumCode() in (25, 26, 27, 28):
                while len(operList) != 0 and precedence[operList[len(operList)-1]] <= precedence[lexeme.getLexStr()]:
                    lexemeList.append(
                        Lexeme(operList[len(operList)-1], Token.findToken(operList.pop())))
                operList.append(lexeme.getLexStr())

        while len(operList) != 0:
            lexemeList.append(
                Lexeme(operList[len(operList) - 1], Token.findToken(operList.pop())))

        postList = []

        for lexeme in lexemeList:
            if lexeme.getToken() is Token.MULT:
                self.multiplication(postList)
            elif lexeme.getToken() is Token.DIV:
                self.division(postList)
            elif lexeme.getToken() is Token.ADD:
                self.addition(postList)
            elif lexeme.getToken() is Token.SUB:
                self.subtraction(postList)
            else:
                postList.append(lexeme.getLexStr())
        return postList.pop()

    # Multiplies the two top elements in postList
    def multiplication(self, postList):
        v2 = postList.pop()
        v1 = postList.pop()
        x1 = None
        x2 = None

        # Find value of first variable
        if Token.findToken(v1) is Token.LITERALINT:
            x1 = int(v1)
        elif Token.findToken(v1) is Token.LITERALFLOAT:
            x1 = float(v1)
        else:
            v1Type = self.getVarType(v1)
            if v1Type is Token.INTEGER:
                x1 = int(self.getVarValue(v1))
            elif v1Type is Token.FLOAT:
                x1 = float(self.getVarValue(v1))

        # Find value of second variable
        if Token.findToken(v2) is Token.LITERALINT:
            x2 = int(v2)
        elif Token.findToken(v2) is Token.LITERALFLOAT:
            x2 = float(v2)
        else:
            v2Type = self.getVarType(v2)
            if v2Type is Token.INTEGER:
                x2 = int(self.getVarValue(v2))
            elif v2Type is Token.FLOAT:
                x2 = float(self.getVarValue(v2))

        result = x1 * x2
        postList.append(str(result))

    # Divides the two top elements in postList
    def division(self, postList):
        v2 = postList.pop()
        v1 = postList.pop()

        x1 = None
        x2 = None

        # Find value of first variable
        if Token.findToken(v1) is Token.LITERALINT:
            x1 = int(v1)
        elif Token.findToken(v1) is Token.LITERALFLOAT:
            x1 = float(v1)
        else:
            v1Type = self.getVarType(v1)
            if v1Type is Token.INTEGER:
                x1 = int(self.getVarValue(v1))
            elif v1Type is Token.FLOAT:
                x1 = float(self.getVarValue(v1))

        # Find value of second variable
        if Token.findToken(v2) is Token.LITERALINT:
            x2 = int(v2)
        elif Token.findToken(v2) is Token.LITERALFLOAT:
            x2 = float(v2)
        else:
            v2Type = self.getVarType(v2)
            if v2Type is Token.INTEGER:
                x2 = int(self.getVarValue(v2))
            elif v2Type is Token.FLOAT:
                x2 = float(self.getVarValue(v2))

        result = x1 / x2
        postList.append(str(result))

    # Adds the two top elements in postList
    def addition(self, postList):
        v2 = postList.pop()
        v1 = postList.pop()

        x1 = None
        x2 = None

        # Find value of first variable
        if Token.findToken(v1) is Token.LITERALINT:
            x1 = int(v1)
        elif Token.findToken(v1) is Token.LITERALFLOAT:
            x1 = float(v1)
        else:
            v1Type = self.getVarType(v1)
            if v1Type is Token.INTEGER:
                x1 = int(self.getVarValue(v1))
            elif v1Type is Token.FLOAT:
                x1 = float(self.getVarValue(v1))

        # Find value of second variable
        if Token.findToken(v2) is Token.LITERALINT:
            x2 = int(v2)
        elif Token.findToken(v2) is Token.LITERALFLOAT:
            x2 = float(v2)
        else:
            v2Type = self.getVarType(v2)
            if v2Type is Token.INTEGER:
                x2 = int(self.getVarValue(v2))
            elif v2Type is Token.FLOAT:
                x2 = float(self.getVarValue(v2))

        result = x1 + x2
        postList.append(str(result))

    # Subtracts the two top elements in postList
    def subtraction(self, postList):
        v2 = postList.pop()
        v1 = postList.pop()

        x1 = None
        x2 = None

        # Find value of first variable
        if Token.findToken(v1) is Token.LITERALINT:
            x1 = int(v1)
        elif Token.findToken(v1) is Token.LITERALFLOAT:
            x1 = float(v1)
        else:
            v1Type = self.getVarType(v1)
            if v1Type is Token.INTEGER:
                x1 = int(self.getVarValue(v1))
            elif v1Type is Token.FLOAT:
                x1 = float(self.getVarValue(v1))

        # Find value of second variable
        if Token.findToken(v2) is Token.LITERALINT:
            x2 = int(v2)
        elif Token.findToken(v2) is Token.LITERALFLOAT:
            x2 = float(v2)
        else:
            v2Type = self.getVarType(v2)
            if v2Type is Token.INTEGER:
                x2 = int(self.getVarValue(v2))
            elif v2Type is Token.FLOAT:
                x2 = float(self.getVarValue(v2))

        result = x1 * x2
        postList.append(str(result))

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
