# CS 4308
# Group Members: Nic Ott, Jason Paek, Sam Perez
# to run this in a terminal, use the command "python -i scanner.py" in this directory
# (Syntax for Dictionary) <keep for now> keywordList = {"function": "def", "define": "="}

# To print, we want the output to be
# Keywords: kw1, kw2, kw3, kw4, kww5, kw6...
# Identifiers: id1, id2, id3, id4, id5, id6...
# Operators: o1, o2, o3, o4, o5, o6...
#
# To do so, the file needs to be scanned line by line, each word read, and the keywords/identifiers/operators
# need to be added to an array(potentially of strings) into an array.
#
# To print
# grab keywords from keywords.txt

# Create 3 lists to define the keywords, operators, and identifiers
Keywords = []
Operators = []
VariableNames = []
Constants = []

# Create 3 lists to compile all the K.O.I found in the .scl files
keyWordsFound = []
operatorsFound = []
variableNamesFound = []
constantsFound = []


# where filePath is a function parameter that's just a file name
def scanner(filePath):
    kwfile = open("keywords.txt")
    for line in kwfile:
        Keywords.append(line.strip())

    opfile = open("operators.txt")
    for line in opfile:
        Operators.append(line.strip())

    idfile = open("identifiers.txt")
    for line in idfile:
        VariableNames.append(line.strip())

    csfile = open("constants.txt")
    for line in csfile:
        Constants.append(line.strip())

    file = open(filePath)
    descriptionComment = False
    varNamesThere = False

    # for each syntax for every line in the file
    for line in file:

        varNameHere = False
        stringyBoy = False

        # splits lines into individual words
        lineList = line.split()

        if len(lineList) == 0:
            continue

        if varNamesThere:
            VariableNames.append(lineList[0])

        for word in lineList:
            # word.strip() gives us the word without whitespace, we can use this to compare 
            # against keywords, operators, variables
            stripped = word.strip()
            stripped = stripped.translate(None, ',')

            # singleline comments in this language start with "//"
            if stripped == "//":
                break

            # multiline comments in this language start with "description" and end with "*/"
            if descriptionComment:
                if stripped == "*/":
                    descriptionComment = False
                continue

            #strings!
            if stringyBoy:
                continue

            if '"' in stripped or "'" in stripped:
                stringyBoy = not stringyBoy
                continue

            if stripped == "description":
                descriptionComment = True

            if stripped == "parameters":
                varNamesThere = True

            if stripped == "specifications":
                varNamesThere = False

            # symbol and define are used to create a variable, so set the value after symbol, 
            # define, or method to a variable name
            if varNameHere:
                VariableNames.append(stripped)
                varNameHere = False

            if stripped == "symbol" or stripped == "define" or stripped == "method":
                varNameHere = True

            if stripped in Keywords:
                #print("Keyword found: " + stripped)
                keyWordsFound.append(stripped)
            elif stripped in Operators:
                #print("Operator found: " + stripped)
                operatorsFound.append(stripped)
            elif stripped in VariableNames:
                #print("Variable found:" + stripped)
                variableNamesFound.append(stripped)
            elif stripped in Constants:
                constantsFound.append(stripped)
            else:
                print(stripped)

    # prints the sequential K.O.I lists to see which words have been identified
    print "\nKeywords Found: ", keyWordsFound, "\n"
    print "Identifiers Found: ", variableNamesFound, "\n"
    print "Operators Found: ", operatorsFound, "\n"
    print "Constants Found: ", constantsFound, "\n"
    return file.name


# gets the name of the file and ends the function
scanner("test.scl")
scanner("arduino_ex1.scl")
scanner("arrayex1b.scl")
scanner("bitops1.scl")
scanner("datablistp.scl")
scanner("linkedg.scl")
scanner("welcome.scl")
