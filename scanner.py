# to run this in a terminal, use the command "python -i scanner.py" in this directory
# (Jason Keep) keywordList = {"function": "def", "define": "="}
Keywords = ["function", "define"]
Operators = []
VariableNames = []

keyWordsFound = []
operatorsFound = []
variableNames = []
# where filePath is a function parameter that's just a file name
def scanner(filePath):

    # open file located at filePath, assign to variable file
    file = open(filePath)

    # for each syntax for every line in the file
    for line in file:
        print(line)  # print the line. duh.
    for keywordItem in Keywords:
        for 
     print (keywordItem)

    # gets the name of the file and ends the function
    return file.name



scanner("test.scl")