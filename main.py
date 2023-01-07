import sys
import subprocess
import lexer

iotaCounter= 0

def iota(resetCounter= False):

    global iotaCounter
    if(resetCounter):
        iotaCounter= 0

    currentValue= iotaCounter
    iotaCounter += 1

    return currentValue

#* stack operations
PUSH_OPERATION= iota(True)
PLUS_OPERATION= iota( )
MINUS_OPERATION= iota( )
DUMP_OPERATION= iota( )
EQUALITY_COMPARISON_OPERATION= iota( )
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

def parseTokenAsPorthOperation(token):
    assert OPERATION_COUNT == 5, "exhaustive handling of operation types in parseTokenAsPorthOperation( )"

    (filePath, rowNumber, startingPosition, word)= token

    if word  == '+':
        return createPlusOperation( )

    elif word == '-':
        return createMinusPlusOperation( )

    elif word == '.':
        return createDumpOperation( )

    elif word == '=':
        return createEqualityComparisonOperation( )

    else:
        try:
            return createPushOperation(int(word))

        except ValueError as valueError:
            print("error in file %s, row number %d and column number %d" % (filePath, rowNumber + 1, startingPosition + 1))
            print(valueError)

            exit(1)

def parsePorthProgram(programFilePath):
    return [
        parseTokenAsPorthOperation(token) for token in lexer.lexFile(programFilePath)
    ]

def leftPopFromList(list):
    return (list[0], list[1:])

def compilePorthProgram(program):
    with open("output.asm", "w") as assemblyOutputFile:

        #* beginning text section of the compiled assembly program and defining the entrypoint
        assemblyOutputFile.write(
            """
                segment .text

                ;;* pops top value out of stack and prints it to the console
                dump:
                    push    rbp
                    mov     rbp, rsp
                    sub     rsp, 64
                    mov     QWORD [rbp-56], rdi
                    mov     QWORD [rbp-8], 0
                    mov     eax, 31
                    sub     rax, QWORD [rbp-8]
                    mov     BYTE [rbp-48+rax], 10
                    add     QWORD [rbp-8], 1
                .L2:
                    mov     rcx, QWORD [rbp-56]
                    mov     rdx, -3689348814741910323
                    mov     rax, rcx
                    mul     rdx
                    shr     rdx, 3
                    mov     rax, rdx
                    sal     rax, 2
                    add     rax, rdx
                    add     rax, rax
                    sub     rcx, rax
                    mov     rdx, rcx
                    mov     eax, edx
                    lea     edx, [rax+48]
                    mov     eax, 31
                    sub     rax, QWORD [rbp-8]
                    mov     BYTE [rbp-48+rax], dl
                    add     QWORD [rbp-8], 1
                    mov     rax, QWORD [rbp-56]
                    mov     rdx, -3689348814741910323
                    mul     rdx
                    mov     rax, rdx
                    shr     rax, 3
                    mov     QWORD [rbp-56], rax
                    cmp     QWORD [rbp-56], 0
                    jne     .L2
                    mov     eax, 32
                    sub     rax, QWORD [rbp-8]
                    lea     rdx, [rbp-48]
                    lea     rcx, [rdx+rax]
                    mov     rax, QWORD [rbp-8]
                    mov     rdx, rax
                    mov     rsi, rcx
                    mov     edi, 1
                    mov     rax, 1
                    syscall
                    nop
                    leave
                    ret

                global _start
                _start:
            """
        )

        #! generating assembly code for the stack operations of the submitted porth code

        for instruction in program:
            assert OPERATION_COUNT == 5, "exhaustive handling of operation types in compilePorthProgram( )"

            if instruction[0] == PUSH_OPERATION:
                assemblyOutputFile.write("""
                    ;; pushing %d to the stack
                    push %d\n
                """ % (instruction[1], instruction[1]))
            
            elif instruction[0] == PLUS_OPERATION:
                assemblyOutputFile.write(
                    """
                    ;; performing plus operation
                    pop rax
                    pop rbx
                    add rax, rbx
                    push rax
                    """
                )

            elif instruction[0] == MINUS_OPERATION:
                assemblyOutputFile.write(
                    """
                    ;; performing minus operation
                    pop rax
                    pop rbx
                    sub rbx, rax
                    push rbx
                    """
                )

            elif instruction[0] == DUMP_OPERATION:
                assemblyOutputFile.write(
                    """
                    ;; performing dump operation
                    pop rdi
                    call dump
                    """
                )

            elif instruction[0] == EQUALITY_COMPARISON_OPERATION:
                assemblyOutputFile.write(
                    """
                    ;; performing equality comparison operation
                    mov rcx, 0
                    mov rdx, 1
                    pop rax
                    pop rbx
                    cmp rax, rbx
                    cmove rcx, rdx
                    """
                )

            else:
                assert False, "can't compile invalid code"

        #* exiting from the compiled assembly program with an exit code of 0
        assemblyOutputFile.write(
            """\n
                    mov rax, 60
                    mov rdi, 0
                    syscall
            """
        )

    subprocess.call(["chmod", "+x", "./compile.sh"])
    subprocess.call(["./compile.sh"])

if __name__ == "__main__":
    argv= sys.argv
    (_, argv)= leftPopFromList(argv)

    if len(argv) < 1:
        print("ERROR: no porth file path provided")

    (porthFilePath, argv)= leftPopFromList(argv)

    sourcecode= parsePorthProgram(porthFilePath)
    compilePorthProgram(sourcecode)