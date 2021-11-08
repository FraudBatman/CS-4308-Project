# CS 4308
# Group Members: Nic Ott, Jason Paek, Sam Perez
# Parser program to our scanner
# The Parser takes input data, typically a file, and builds tree or hierarchial structure

# Giving a structural representation of the input while checking for correct syntax.
# Refer to scl_grammar.txt for grammar
# utilizes Lexier and Token from the lexier.py file

# This parser is able to take any file as input text, we used "test.scl" as test input

from scanner import *
from node import *

# Main Parser class


class Parser:
    lexier = Lexier()
    token = Token()
    nextToken = None

    # def __init__(self, lexemeList):   Constructor
    def fileTime(self, filePath):
        root = Node(None, None, Type.PROGRAM)
        file = open(filePath)  # Opens the file sent in
        for line in file:  # Compules the file line by line
            # Sends it to the parser file for compilation
            self.compile(line, root)
        return root  # returns the root for the interpreter to do its magic

# Compile function
    def compile(self, input, root):
        # Takes input and sends it to a lexier analyzer
        layer = 1
        # creates the node for the start of the line
        root.add_c_node(Node(root, layer, Type.IMPLEMENT))
        self.lexier.analyzer(input)
        self.getNextToken()  # Gets the next token after the input
        # Gets the keyword from the input files
        self.keywords(root.getChildren()[-1], layer)

    # Keywords function
    def keywords(self, node, layer):
        layer += 1  # increments the layer
        # Prints to show that it was being tested as a keyword
        print("Entering <keywords>")
        # Sends to the term function to determine if it is also an identifier
        self.identifier(node, layer)
        while(self.nextToken.TYPE == self.lexier.ADD_OP or self.nextToken.TYPE == self.lexier.SUB_OP):
            self.getNextToken()  # If it is a keyword, it will print the keyword
            # adds the keyword as a child of the parent node
            node.add_c_node(Node(node, layer, Type.KEYWORDS))
            children = node.getChildren()
            # It will also send to the identifier function
            self.identifier(children[-1], layer)
        print("Exiting <keywords>")

    # Identifier function
    def identifier(self, node, layer):
        layer += 1  # increments the layer
        # Prints to show that it was being tested as an identifier
        print("Entering <identifier>")
        # Sends to the operator function to determine if this is also an operator
        self.operators(node, layer)
        while(self.nextToken.TYPE == self.lexier.MULT_OP or self.nextToken.TYPE == self.lexier.DIV_OP):
            self.getNextToken()  # If it is an identifier, it will print the term
            # adds the identifer as a child of the parent node
            node.add_c_node(Node(node, layer, Type.IDENTIFIER))
            children = node.getChildren()
            # It will also send to the operator method
            self.operators(children[0], layer)
        # Once all identifiers have been determined it will exit the identifier function
        print("Exiting <identifier>")

    # Operators function
    def operators(self, node, layer):
        layer += 1
        # Prints to show that it was being tested as an operator
        print("Entering <operators>")
        if(self.nextToken.TYPE == self.lexier.IDENT or self.nextToken.TYPE == self.lexier.INT_LIT):
            self.getNextToken()  # Will get the next token if it is an operator
            # adds the operator as a child of the parent node
            node.add_c_node(Node(node, layer, Type.OPERATORS))
        else:
            # If it isnt an operator it will get the next token and send to the expression function
            if(self.nextToken.TYPE == self.lexier.LEFT_PAREN):
                self.getNextToken()  # get the next token and send to the keywords function
                node.add_c_node(Node(node, layer, Type.OPERATORS))
                self.keywords(node.getChildren()[-1], layer)
                if(self.nextToken.TYPE == self.lexier.RIGHT_PAREN):
                    self.getNextToken()
                    node.add_c_node(Node(node, layer, Type.OPERATORS))
                else:
                    self.error()
        # Once all terms have been determined it will exit the operators function
        print("Exiting <operators>")

    # Get next token
    def getNextToken(self):
        self.nextToken = self.lexier.getNext()

    # Function to print error
    def error(self):
        print("Syntax error")

# parser = Parser()

# # Method/Class to get input for the file
# txtFile = input("Type in a file(insert quotation marks around the file): ")

# #The file is only sent to the parser method if it is not empty
# #This does not take nonexistance of a file into consideration
# if (txtFile == ""):
#     print("Empty Input, Please input a valid file.")
# else:
#     parser.fileTime(txtFile)
