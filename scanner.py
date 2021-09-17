# to run this in a terminal, use the command "python -i scanner.py" in this directory
# (Jason Keep) keywordList = {"function": "def", "define": "="}
Keywords = []
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

    # grab keywords from keywords.txt
    kwfile = open("keywords.txt")
    for line in kwfile:
        Keywords.append(line)

        # open file located at filePath, assign to variable file
    file = open(filePath)
    descriptionComment = False

    # for each syntax for every line in the file
    for line in file:
        varNameHere = False

        # splits lines into individual words
        lineList = line.split()
        for word in lineList:
            # word.strip() gives us the word without whitespace, we can use this to compare against keywords, operators, variables
            stripped = word.strip()

            # singleline comments in this language start with "//"
            if stripped == "//":
                break

            # multiline comments in this language start with "description" and end with "*/"
            if descriptionComment:
                if stripped == "*/":
                    descriptionComment = False
                continue

            if stripped == "description":
                descriptionComment = True

            # symbol and define are used to create a variable, so set the value after symbol or define to a variable name
            if varNameHere:
                VariableNames.append(stripped)
                varNameHere = False

            if stripped == "symbol" or stripped == "define":
                varNameHere = True

            if stripped in Keywords:
                print("Keyword found: " + stripped)
                keyWordsFound.append(stripped)
            elif stripped in Operators:
                print("Operator found: " + stripped)
                operatorsFound.append(stripped)
            elif stripped in VariableNames:
                print("Variable found:" + stripped)
                variableNames.append(stripped)
            else:
                print(stripped)

    # gets the name of the file and ends the function
    return file.name


scanner("test.scl")
