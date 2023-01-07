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
        return [(filePath, lineNumber, startingPosition, word)

            # extracting lines from the file
            for (lineNumber, line) in enumerate(file.readlines( ))

            # extracting characters from a line
            for (startingPosition, word) in lexLine(line)
        ]