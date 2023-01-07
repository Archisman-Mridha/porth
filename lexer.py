import interpreter

# add reference of end statement in the related if operation
def resolveCrossReferences(interpretedSourcecode):
    assert interpreter.OPERATION_COUNT == 7, "exhaustive handling of operation types in getCrossReferences( )"

    stack= [ ]

    for index in range(len(interpretedSourcecode)):
        operation= interpretedSourcecode[index]

        if operation[0] == interpreter.IF_OPERATION:
            stack.append(index)

        elif operation[0] == interpreter.BLOCK_END_OPERATION:
            relatedIfOperationIndex= stack.pop( ) # getting index of the if operation which is related to this end statement
            assert interpretedSourcecode[relatedIfOperationIndex][0] == interpreter.IF_OPERATION, "no if block found for end keyword"

            # referncing index of the end statement in the related if operation
            interpretedSourcecode[relatedIfOperationIndex]= (interpreter.IF_OPERATION, index)

    return interpretedSourcecode

def findStartingColumnNumberAfterPredicate(line, startingPosition, isCharacterPredicate):
    currentPosition= startingPosition

    while currentPosition < len(line) and not isCharacterPredicate(line[currentPosition]):
        currentPosition += 1

    return currentPosition

def lexLine(line):
    # ignore whitespaces in the beginning of the line
    wordStartingPosition= findStartingColumnNumberAfterPredicate(line, 0,
                                                                    lambda character: not character.isspace( ))

    while wordStartingPosition < len(line):

        # find position of the next whitespace
        nextWhitespaceStartingPosition= findStartingColumnNumberAfterPredicate(line, wordStartingPosition,
                                                                                lambda character: character.isspace( ))

        word= line[wordStartingPosition:nextWhitespaceStartingPosition]
        yield (wordStartingPosition, word)

        wordStartingPosition= findStartingColumnNumberAfterPredicate(line, nextWhitespaceStartingPosition,
                                                                        lambda character: not character.isspace( ))

def lexFile(filePath):
    with open(filePath, "r") as file:

        # iterating through the lines
        for (lineNumber, line) in enumerate(file.readlines( )):

            # iterating through words in the line
            for (startingPosition, word) in lexLine(line):
                yield (filePath, lineNumber, startingPosition, word)