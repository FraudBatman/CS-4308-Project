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
        self.lexier.analyzer(input) #Takes input and sends it to a lexier analyzer
        self.getNextToken()         #Gets the next token after the input
        self.keywords()                 #Gets the keyword from the input files

    # Keywords function
    def keywords(self):
        print("Entering <keywords>")   #Prints to show that it was being tested as a keyword
        self.identifier() #Sends to the term function to determine if it is also an identifier
        while(self.nextToken.TYPE == self.lexier.ADD_OP or self.nextToken.TYPE == self.lexier.SUB_OP):
            self.getNextToken() #If it is a keyword, it will print the keyword
            self.identifier()         #It will also send to the term function
        print("Exiting <keywords>")

    #Identifier function
    def identifier(self):
        print("Entering <term>")   #Prints to show that it was being tested as an identifier
        self.operator() #Sends to the operator function to determine if this is also an operator
        while(self.nextToken.TYPE == self.lexier.MULT_OP or self.nextToken.TYPE == self.lexier.DIV_OP):
            self.getNextToken()             #If it is an identifier, it will print the term
            self.operator()                   #It will also send to the operator method 
        print("Exiting <term>")                #Once all identifiers have been determined it will exit the identifier function

    # Operators function
    def operators(self):      
        print("Entering <operators>") #Prints to show that it was being tested as an operator
        if(self.nextToken.TYPE == self.lexier.IDENT or self.nextToken.TYPE == self.lexier.INT_LIT):
            self.getNextToken()     #Will get the next token if it is an operator
        else:
            if(self.nextToken.TYPE == self.lexier.LEFT_PAREN):  #If it isnt an operator it will get the next token and send to the expression function
                self.getNextToken()                             #get the next token and send to the keywords function
                self.keywords()
                if(self.nextToken.TYPE == self.lexier.RIGHT_PAREN): 
                    self.getNextToken()
                else:
                    self.error()
        print("Exiting <factor>")  #Once all terms have been determined it will exit the factor function

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


