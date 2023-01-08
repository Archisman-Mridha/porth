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
IF_OPERATION= iota( )
ELSE_OPERATION= iota( )
BLOCK_END_OPERATION= iota( )
DUP_OPERATION= iota( ) #* `dup` operation, creates a duplicate of the value at the top of the stack and pushes that duplicate to the top of the stack
GREATER_THAN_COMPARISON_OPERATION= iota( )
WHILE_OPERATION= iota( )
DO_OPERATION= iota( )
MEM_OPERATION= iota( ) #* `mem` operation, pushes the beginning of the memory where you can read and write, to the stack
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

def parseTokenAsPorthOperation(token):
    assert OPERATION_COUNT == 13, "exhaustive handling of operation types in parseTokenAsPorthOperation( )"

    (filePath, rowNumber, startingPosition, word)= token

    if word  == '+':
        return createPlusOperation( )

    elif word == '-':
        return createMinusPlusOperation( )

    elif word == 'dump':
        return createDumpOperation( )

    elif word == '=':
        return createEqualityComparisonOperation( )

    elif word == 'if':
        return createIfOperation( )

    elif word == 'else':
        return createElseOperation( )

    elif word == 'end':
        return createBlockEndOperation( )

    elif word == 'dup':
        return createDupOperation( )

    elif word == '>':
        return createGreaterThanComparisonOperation( )

    elif word == 'do':
        return createDoOperation( )

    elif word == 'while':
        return createWhileOperation( )

    elif word == 'mem':
        return createMemOperation( )

    else:
        try:
            return createPushOperation(int(word))

        except ValueError as valueError:
            print("error in file %s, row number %d and column number %d" % (filePath, rowNumber + 1, startingPosition + 1))
            print(valueError)

            sys.exit(1)

def parsePorthProgram(programFilePath):
    return lexer.resolveCrossReferences(
        [ parseTokenAsPorthOperation(token) for token in lexer.lexFile(programFilePath) ]
    )

def leftPopFromList(list):
    return (list[0], list[1:])

def compilePorthProgram(program):
    with open("output.asm", "w") as assemblyOutputFile:

        #* beginning text section of the compiled assembly program and defining the entrypoint
        assemblyOutputFile.write(
            """
            segment .bss
                ;;* allocating some memory where user can read or write data
                mem: resb 500000

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

        for index in range(len(program)):
            assert OPERATION_COUNT == 13, "exhaustive handling of operation types in compilePorthProgram( )"

            instruction= program[index]

            assemblyOutputFile.write(
                """
                    addr_%d:
                """ % index
            )

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
                        pop rbx
                        pop rax
                        cmp rax, rbx
                        cmove rcx, rdx
                        push rcx
                    """
                )

            elif instruction[0] == IF_OPERATION:
                assert len(instruction) >= 2, "end statement not found for if block"

                assemblyOutputFile.write(
                    """
                        ;; handling if block
                        pop rax
                        test rax, rax
                        jz addr_%d
                    """ % instruction[1]
                )

            elif instruction[0] == ELSE_OPERATION:
                assemblyOutputFile.write(
                    """
                        ;; handling else statement
                        jmp addr_%d
                    """ % (instruction[1], index+1)
                )

            elif instruction[0] == BLOCK_END_OPERATION:
                assert len(instruction) >= 2, "end statement should have reference to the next instruction to jump to"

                assemblyOutputFile.write(
                    """
                        ;; handling end statement
                    """
                )

                if index + 1 != instruction[1]:
                    assemblyOutputFile.write(
                        """
                        jmp addr_%d
                        """ % instruction[1]
                    )

            elif instruction[0] == DUP_OPERATION:
                assemblyOutputFile.write(
                    """
                        ;; performing dup operation
                        pop rax
                        push rax
                        push rax
                    """
                )

            elif instruction[0] == GREATER_THAN_COMPARISON_OPERATION:
                assemblyOutputFile.write(
                    """
                        ;; performing greater than comparison operation
                        mov rcx, 0
                        mov rdx, 1
                        pop rbx
                        pop rax
                        cmp rax, rbx
                        cmovg rcx, rdx
                        push rcx
                    """
                )

            elif instruction[0] == WHILE_OPERATION:
                pass

            elif instruction[0] == DO_OPERATION:
                assert len(instruction) >= 2, "do operation doesn't have reference to the end statement"

                assemblyOutputFile.write(
                    """
                        ;; performing do operation
                        pop rax
                        test rax, rax
                        jz addr_%d
                    """ % instruction[1]
                )

            elif instruction[0] == MEM_OPERATION:
                assemblyOutputFile.write(
                    """
                        push mem
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

    interpretedSourcecode= parsePorthProgram(porthFilePath)
    compilePorthProgram(interpretedSourcecode)