from utils import iota

#* stack operations
PUSH_OPERATION= iota(True)
PLUS_OPERATION= iota( )
MINUS_OPERATION= iota( )
DUMP_OPERATION= iota( )
EQUALITY_COMPARISON_OPERATION= iota( )
IF_OPERATION= iota( )
ELSE_OPERATION= iota( )
BLOCK_END_OPERATION= iota( )
DUP_OPERATION= iota( ) #* `dup` operation, creates a duplicate of the value at the top of the stack and pushes that duplicate to the top of the stack
GREATER_THAN_COMPARISON_OPERATION= iota( )
WHILE_OPERATION= iota( )
DO_OPERATION= iota( )
MEM_OPERATION= iota( ) #* `mem` operation, pushes the beginning of the memory where you can read and write, to the stack
WRITE_TO_MEM_OPERATION= iota( )
READ_FROM_MEM_OPERATION= iota( )
SYSCALL_OPERATION= iota( ) #! incomplete support
OPERATION_COUNT= iota( )

def createPushOperation(value):
    return (PUSH_OPERATION, value)

def createPlusOperation( ):
    return (PLUS_OPERATION, )

def createMinusPlusOperation( ):
    return (MINUS_OPERATION, )

def createDumpOperation( ):
    return (DUMP_OPERATION, )

def createEqualityComparisonOperation( ):
    return (EQUALITY_COMPARISON_OPERATION, )

def createIfOperation( ):
    return (IF_OPERATION, )

def createElseOperation( ):
    return (ELSE_OPERATION, )

def createBlockEndOperation( ):
    return (BLOCK_END_OPERATION, )

def createDupOperation( ):
    return (DUP_OPERATION, )

def createGreaterThanComparisonOperation( ):
    return (GREATER_THAN_COMPARISON_OPERATION, )

def createDoOperation( ):
    return (DO_OPERATION, )

def createWhileOperation( ):
    return (WHILE_OPERATION, )

def createMemOperation( ):
    return (MEM_OPERATION, )

def createWriteToMemOperation( ):
    return (WRITE_TO_MEM_OPERATION, )

def createReadFromMemOperation( ):
    return (READ_FROM_MEM_OPERATION, )

def createSyscallOperation( ):
    return (SYSCALL_OPERATION, )