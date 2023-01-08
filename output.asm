
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
            
                    addr_0:
                
                        ;; pushing 10 to the stack
                        push 10

                
                    addr_1:
                
                    addr_2:
                
                        ;; performing dup operation
                        pop rax
                        push rax
                        push rax
                    
                    addr_3:
                
                        ;; pushing 0 to the stack
                        push 0

                
                    addr_4:
                
                        ;; performing greater than comparison operation
                        mov rcx, 0
                        mov rdx, 1
                        pop rbx
                        pop rax
                        cmp rax, rbx
                        cmovg rcx, rdx
                        push rcx
                    
                    addr_5:
                
                        ;; performing do operation
                        pop rax
                        test rax, rax
                        jz addr_11
                    
                    addr_6:
                
                        ;; performing dup operation
                        pop rax
                        push rax
                        push rax
                    
                    addr_7:
                
                        ;; performing dump operation
                        pop rdi
                        call dump
                    
                    addr_8:
                
                        ;; pushing 1 to the stack
                        push 1

                
                    addr_9:
                
                        ;; performing minus operation
                        pop rax
                        pop rbx
                        sub rbx, rax
                        push rbx
                    
                    addr_10:
                
                        ;; handling end statement
                    
                        jmp addr_1
                        
                    addr_11:
                
                        ;; pushing 420 to the stack
                        push 420

                
                    addr_12:
                
                        ;; performing dump operation
                        pop rdi
                        call dump
                    

                    mov rax, 60
                    mov rdi, 0
                    syscall
            