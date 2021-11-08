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
        self.vars = {}
        self.cons = {}
        self.var_input = {}
        self.cons_input = {}

    # Interpreter method
    def interpret(self, filePath):
        print("Parsing SCL File", "\n")
        parser = Parser()
        parseTree = parser.fileTime(filePath)
        print("\nFinished Parsing SCL File")
        print("="*50, "\n")

        # Switch statement to run through all the node's direct children
        for node in parseTree.getChildren():
            if node.getType() is Type.IMPORT:   # ignore if node is import
                pass
            elif node.getType() is Type.SYMBOL: # ignore if node is symbol
                pass
            elif node.getType() is Type.DEFAULTS: #interpret the node as a default if is a part of default
                self.interp_default(node)
            elif node.getType() is Type.IMPLEMENT: # interpret if node is an implementation
                self.interp_imp(node)



    # The following methods interpret tokens
    #
    # default tokens
    def interp_default(self, node): #default interpreter
        for child in node.getChildren():    #Gets the child of each child node
            if child.getType() is Type.CONST_DEC:   #If the child is a constant declaration
                self.interp_const_declaration(child) # then interpret it
            elif child.getType() is Type.IDENTIFIER: # If the child is an identifier
                self.interp_ident(child)             # interpret the identifier 

    # implementation
    def interp_imp(self, node):
        if node.getChildren() == None:      #If the implication has no children
            return                          #Skip
        for child in node.getChildren():    #If it isnt empty get child of each child node
            if child.getType() is Type.KEYWORDS: #If the child is a keyword
                self.interp_keys(child)     #interpret the keyword

    # constant declarations
    def interp_const_declaration(self, node):
        for child in node.getChildren():    #Get the children of the declaration(should only be one)
            if child.getType() is Type.CONST_LIST: #If the child is a constants list
                self.interp_c_list(child)           # interpret it
#####################################################################################################
#####################################################################################################

    # constants 
    def interp_c_list(self, node):
        for child in node.getChildren():    #get the children of the constants list
            if child.getType() is Type.COMP_DECLARE:    #if the child is a complete declaration
                self.interp_comp_dec(child)             #interpret it

    # indentifier
    def interp_ident(self, node): 
        for child in node.getChildren():    #get the children of the identifiers
            if child.getType() is Type.VAR_LIST:    #if the child is a variable list
                self.interpretVarList(child)    #interpret it
#####################################################################################################
#####################################################################################################

    # variable list
    def interpretVarList(self, node):
        for child in node.getChildren():    #get the children of the variable list
            if child.getType() is Type.COMP_DECLARE:    #if the child is a complete declaration
                self.interp_comp_dec(child)         #interpret it

    # complete declarations
    def interp_comp_dec(self, node):    #interprets the node
        parent = node.getParent()       #retrieve the parent node 
        third_parent = parent.getParent().getParent()   #retrieve the parent node of the parent node

        #if the parent type is a constansts list, then the node is a constant 
        isConstant = True if parent.getType() is Type.CONST_LIST else False 
        #if the parent of the parents node is a default node, then the node is a default also
        isDefault = True if third_parent.getType() is Type.DEFAULTS else False

        lex = node.getScanLine().getLex()   #scans the line of each node
        token_type = None

        for child in node.getChildren():    #get the children nodes
            if child.getType() is Type.RET_TYPE:    #If it is a return node
                token_type = self.interp_return(child)  #Interpret it

        if isDefault is True:       #check if the node is a default token
            if isConstant is True:  #if it is, check if it is also a constant
                self.cons[lex[1].getLexStr()] = [lex[3].getLexStr(), token_type] #if it is create a const in the form of a string 
            else:
                self.vars[lex[1].getLexStr()] = ["", token_type] #if it isnt then create a string in the form of a variable
        else:
            if isConstant is True:  #if it isnt a default token
                self.cons_input[lex[1].getLexStr()] = [lex[3].getLexStr(), token_type]#if it is create a const in the form of a string
            else:
                self.var_input[lex[1].getLexStr()] = ["", token_type]#if it isnt then create a string in the form of a variable
    #
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
            elif child.getType() is Type.PARENTHESIS:
                self.interpret_parenthesis(child)

    # Interprets parenthesis operations
    def interpret_parenthesis(self, node):
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
            if lexeme.getToken().getNumCode():
                returnString += str(self.getVarValue(lexeme.getLexStr()))
            # Compares if it is string ident or const string ident 
            elif lexeme.getToken().getNumCode():
                returnString += str(self.getLitStr(self.getVarValue(lexeme.getLexStr())))
            # Compares if a token is not a string literal
            elif lexeme.getToken().getNumCode():
                returnString += str(lexeme.getLexStr())
            # Compares if a token is a string literal
            elif lexeme.getToken() is Token.STRING_LITERAL:
                returnString += str(self.getLitStr(lexeme.getLexStr()))
        return returnString

#####################################################################################################
#####################################################################################################

    # Returns string value which excludes the quotes and comma
    def getLitStr(self, lextr):
        result = re.search("\"(.*)\"", lextr) #Uses regular expressions to find the literal string
        return result.group(1)
#####################################################################################################
#####################################################################################################

    # Interprets exp node and returns expression value
    def interp_exprs(self, node):
        lineLexems = node.getScanLine().getLex()    #Gets the line for the expression

        explex = lineLexems[3:len(lineLexems)]

        # Create a precedence for operands
        precedence = {"*": 1, "/": 1, "+": 2, "-": 2} #PEMDAS

        lexemeList = []     #List of variables
        operList = []       #List of operations

        index = 0           #Index of the list
        exprResult = 0      #Solution to the expression

        for lexeme in explex:
            if lexeme.getToken():   #if the token exists
                lexemeList.append(lexeme)   #then append the token
            elif lexeme.getToken(): #get the token 
                while len(operList) != 0 and precedence[operList[len(operList)-1]] <= precedence[lexeme.getLexStr()]: #determine the precedence of the operation
                    lexemeList.append(Lexeme(operList[len(operList)-1], Token.findToken(operList.pop()))) #append the list at a specific token
                operList.append(lexeme.getLexStr()) #append the lexeme list at the string 

        while len(operList) != 0:   #While the list is not empty
            lexemeList.append(Lexeme(operList[len(operList) - 1], Token.findToken(operList.pop()))) 
            #append the list at a specific token

        postList = []   #List after appendages

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

#####################################################################################################
#####################################################################################################

    # Multiplies the two top elements in postList
    def multiplication(self, postList):
        v2 = postList.pop()
        v1 = postList.pop()
        x1 = None
        x2 = None

        # Find value of first variable
        if Token.findToken(v1) is Token.LITERALINT:     #If the token is an integer
            x1 = int(v1)                #Set it equal to x1
        elif Token.findToken(v1) is Token.LITERALFLOAT:     #If it is a float
            x1 = float(v1)          #Set it to x1
        else:
            v1Type = self.getVarType(v1)        #get variable type
            if v1Type is Token.INTEGER:     #If it is an int
                x1 = int(self.getVarValue(v1))  #set it to x1
            elif v1Type is Token.FLOAT: #If it is a float
                x1 = float(self.getVarValue(v1))    #set it to x1

        # Find value of second variable
        if Token.findToken(v2) is Token.LITERALINT:     #Repeat the same process for x2
            x2 = int(v2)
        elif Token.findToken(v2) is Token.LITERALFLOAT:
            x2 = float(v2)
        else:
            v2Type = self.getVarType(v2)
            if v2Type is Token.INTEGER:
                x2 = int(self.getVarValue(v2))
            elif v2Type is Token.FLOAT:
                x2 = float(self.getVarValue(v2))
                    
        result = x1 * x2        #Multiply the two numbers
        postList.append(str(result))    #add it to the results list
#####################################################################################################
#####################################################################################################
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

#####################################################################################################
#####################################################################################################

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

#####################################################################################################
#####################################################################################################

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
