import interpreter

# add reference of end statement in the related if operation
def resolveCrossReferences(interpretedSourcecode):
    assert interpreter.OPERATION_COUNT == 13, "exhaustive handling of operation types in getCrossReferences( )"

    stack= [ ]

    for index in range(len(interpretedSourcecode)):
        operation= interpretedSourcecode[index]

        if operation[0] == interpreter.IF_OPERATION:
            stack.append(index)

        elif operation[0] == interpreter.ELSE_OPERATION:
            relatedIfOperationIndex= stack.pop( ) # getting index of the related if operation
            assert interpretedSourcecode[relatedIfOperationIndex][0] == interpreter.IF_OPERATION, "`else` can only be used to close if/else blocks"

            interpretedSourcecode[relatedIfOperationIndex]= (interpreter.IF_OPERATION, index + 1)

            stack.append(index)

        elif operation[0] == interpreter.WHILE_OPERATION:
            stack.append(index)

        elif operation[0] == interpreter.DO_OPERATION:
            relatedWhileOperationIndex= stack.pop( )

            # referencing related while operation
            interpretedSourcecode[index]= (interpreter.DO_OPERATION, relatedWhileOperationIndex)

            stack.append(index)

        elif operation[0] == interpreter.BLOCK_END_OPERATION:
            relatedOperationIndex= stack.pop( )

            #* in case of if/else blocks
            if(interpretedSourcecode[relatedOperationIndex][0] == interpreter.IF_OPERATION
                or interpretedSourcecode[relatedOperationIndex][0] == interpreter.ELSE_OPERATION):
                    interpretedSourcecode[relatedOperationIndex]= (interpretedSourcecode[relatedOperationIndex][0], index)

                    # from the end statement we will continue with the next instructions
                    interpretedSourcecode[index]= (interpreter.BLOCK_END_OPERATION, index + 1)

            #* in case of `do` operation in while blocks
            elif interpretedSourcecode[relatedOperationIndex][0] == interpreter.DO_OPERATION:
                assert len(interpretedSourcecode[relatedOperationIndex]) >= 2, "related `do` operation must have refernce to the `while` block"

                # from the `end` statement we will again jump to the `while` statement
                interpretedSourcecode[index]= (interpreter.BLOCK_END_OPERATION, interpretedSourcecode[relatedOperationIndex][1])

                interpretedSourcecode[relatedOperationIndex]= (interpreter.DO_OPERATION, index + 1)

            else:
                raise Exception("`end` can be only be used to close `if/else` or `do` blocks")

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
            for (startingPosition, word) in lexLine(line.split('//')[0]):
                yield (filePath, lineNumber, startingPosition, word)