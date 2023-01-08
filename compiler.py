import operations
import subprocess

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
            assert operations.OPERATION_COUNT == 15, "exhaustive handling of operation types in compilePorthProgram( )"

            instruction= program[index]

            assemblyOutputFile.write(
                """
                    addr_%d:
                """ % index
            )

            if instruction[0] == operations.PUSH_OPERATION:
                assemblyOutputFile.write("""
                        ;; pushing %d to the stack
                        push %d\n
                """ % (instruction[1], instruction[1]))
            
            elif instruction[0] == operations.PLUS_OPERATION:
                assemblyOutputFile.write(
                    """
                        ;; performing plus operation
                        pop rax
                        pop rbx
                        add rax, rbx
                        push rax
                    """
                )

            elif instruction[0] == operations.MINUS_OPERATION:
                assemblyOutputFile.write(
                    """
                        ;; performing minus operation
                        pop rax
                        pop rbx
                        sub rbx, rax
                        push rbx
                    """
                )

            elif instruction[0] == operations.DUMP_OPERATION:
                assemblyOutputFile.write(
                    """
                        ;; performing dump operation
                        pop rdi
                        call dump
                    """
                )

            elif instruction[0] == operations.EQUALITY_COMPARISON_OPERATION:
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

            elif instruction[0] == operations.IF_OPERATION:
                assert len(instruction) >= 2, "end statement not found for if block"

                assemblyOutputFile.write(
                    """
                        ;; handling if block
                        pop rax
                        test rax, rax
                        jz addr_%d
                    """ % instruction[1]
                )

            elif instruction[0] == operations.ELSE_OPERATION:
                assemblyOutputFile.write(
                    """
                        ;; handling else statement
                        jmp addr_%d
                    """ % (instruction[1], index+1)
                )

            elif instruction[0] == operations.BLOCK_END_OPERATION:
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

            elif instruction[0] == operations.DUP_OPERATION:
                assemblyOutputFile.write(
                    """
                        ;; performing dup operation
                        pop rax
                        push rax
                        push rax
                    """
                )

            elif instruction[0] == operations.GREATER_THAN_COMPARISON_OPERATION:
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

            elif instruction[0] == operations.WHILE_OPERATION:
                pass

            elif instruction[0] == operations.DO_OPERATION:
                assert len(instruction) >= 2, "do operation doesn't have reference to the end statement"

                assemblyOutputFile.write(
                    """
                        ;; performing do operation
                        pop rax
                        test rax, rax
                        jz addr_%d
                    """ % instruction[1]
                )

            elif instruction[0] == operations.MEM_OPERATION:
                assemblyOutputFile.write(
                    """
                        push mem
                    """
                )

            elif instruction[0] == operations.READ_FROM_MEM_OPERATION:
                assemblyOutputFile.write(
                    """
                        ;; handling read from mem operation
                        pop rax
                        xor rbx, rbx
                        mov bl, [rax]
                        push rbx
                    """
                )

            elif instruction[0] == operations.WRITE_TO_MEM_OPERATION:
                assemblyOutputFile.write(
                    """
                        ;; handling write to mem operation
                        pop rbx
                        pop rax
                        mov [rax], bl
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