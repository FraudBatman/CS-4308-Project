# CS 4308
# Group Members:Sam Perez
# Parser program to our scanner
# The Parser takes input data, typically a file, and builds tree or hierarchial structure

# Giving a structural representation of the input while checking for correct syntax.
# Refer to scl_grammar.txt for grammar
# utilizes Lexier and Token from the lexier.py file

#This parser is able to take any file as input text, we used "test.scl" as test input

from lexier import Lexier
from lexier import Token

#Main Parser class
class Parser:
    lexier = Lexier()
    token = Token()
    nextToken = None

    # def __init__(self, lexemeList):   Constructor 
    def fileTime(self, filePath):
        file = open(filePath)   #Opens the file sent in
        for line in file:   #Compules the file line by line
            parser.compile(line)    #Sends it to the parser file for compilation

# Compile function
    def compile(self, input):
        self.lexier.analyzer(input)
        self.getNextToken()
        self.expr()

    # Expression function
    def expr(self):
        print("Enter <expr>")
        self.term()
        while(self.nextToken.TYPE == self.lexier.ADD_OP or self.nextToken.TYPE == self.lexier.SUB_OP):
            self.getNextToken()
            self.term()
        print("Exit <expr>")

    #Term function
    def term(self):
        print("Enter <term>")
        self.factor()
        while(self.nextToken.TYPE == self.lexier.MULT_OP or self.nextToken.TYPE == self.lexier.DIV_OP):
            self.getNextToken()
            self.factor()
        print("Exit <term>")

    # Factor function
    def factor(self):
        print("Enter <factor>")
        if(self.nextToken.TYPE == self.lexier.IDENT or self.nextToken.TYPE == self.lexier.INT_LIT):
            self.getNextToken()
        else:
            if(self.nextToken.TYPE == self.lexier.LEFT_PAREN):
                self.getNextToken()
                self.expr()
                if(self.nextToken.TYPE == self.lexier.RIGHT_PAREN):
                    self.getNextToken()
                else:
                    self.error()
        print("Exit <factor>")

    # Get next token
    def getNextToken(self):
        self.nextToken = self.lexier.getNext()

    # Function to print error
    def error(self):
        print("Syntax error")


parser = Parser()

# Method/Class to get input for the file
txtFile = input("Type in a file(insert quotation marks around the file): ") 

#The file is only sent to the parser method if it is not empty
#This does not take nonexistance of a file into consideration
if (txtFile == ""):
    print("Empty Input, Please input a valid file.")
else:
    parser.fileTime(txtFile)


