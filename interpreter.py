import sys
import compiler
import _parser
from utils import leftPopFromList

if __name__ == "__main__":
    argv= sys.argv
    (_, argv)= leftPopFromList(argv)

    if len(argv) < 1:
        print("ERROR: no porth file path provided")

    (porthFilePath, argv)= leftPopFromList(argv)

    interpretedSourcecode= _parser.parsePorthProgram(porthFilePath)
    compiler.compilePorthProgram(interpretedSourcecode)