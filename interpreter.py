import sys
import compiler
import _parser
import utils

if __name__ == "__main__":
    argv= sys.argv
    (_, argv)= utils.leftPopFromList(argv)

    if len(argv) < 1:
        print("ERROR: no porth file path provided")

    (porthFilePath, argv)= utils.leftPopFromList(argv)

    interpretedSourcecode= _parser.parsePorthProgram(porthFilePath)
    compiler.compilePorthProgram(interpretedSourcecode)