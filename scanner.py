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
# Comment :) 
#
# To print, we want the output to be 
# Keywords: kw1, kw2, kw3, kw4, kww5, kw6...
# Identifiers: id1, id2, id3, id4, id5, id6....
#
# To do so, the file needs to be scanned line by line, each word read, and the keywords/identifiers 
# need to be added to an array(potentially of strings) into an array. 
#
# To print 

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