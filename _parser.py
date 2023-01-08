import lexer
import operations
import sys

def parseTokenAsPorthOperation(token):
    assert operations.OPERATION_COUNT == 15, "exhaustive handling of operation types in parseTokenAsPorthOperation( )"

    (filePath, rowNumber, startingPosition, word)= token

    if word  == '+':
        return operations.createPlusOperation( )

    elif word == '-':
        return operations.createMinusPlusOperation( )

    elif word == 'dump':
        return operations.createDumpOperation( )

    elif word == '=':
        return operations.createEqualityComparisonOperation( )

    elif word == 'if':
        return operations.createIfOperation( )

    elif word == 'else':
        return operations.createElseOperation( )

    elif word == 'end':
        return operations.createBlockEndOperation( )

    elif word == 'dup':
        return operations.createDupOperation( )

    elif word == '>':
        return operations.createGreaterThanComparisonOperation( )

    elif word == 'do':
        return operations.createDoOperation( )

    elif word == 'while':
        return operations.createWhileOperation( )

    elif word == 'mem':
        return operations.createMemOperation( )

    elif word == ',':
        return operations.createReadFromMemOperation( )

    elif word == '.':
        return operations.createWriteToMemOperation( )

    else:
        try:
            return operations.createPushOperation(int(word))

        except ValueError as valueError:
            print("error in file %s, row number %d and column number %d" % (filePath, rowNumber + 1, startingPosition + 1))
            print(valueError)

            sys.exit(1)

def parsePorthProgram(programFilePath):
    return lexer.resolveCrossReferences(
        [ parseTokenAsPorthOperation(token) for token in lexer.lexFile(programFilePath) ]
    )