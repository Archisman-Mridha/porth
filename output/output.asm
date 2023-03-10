
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
            
                    addr_0:
                
                        push mem
                    
                    addr_1:
                
                        ;; pushing 0 to the stack
                        push 0

                
                    addr_2:
                
                        ;; performing plus operation
                        pop rax
                        pop rbx
                        add rax, rbx
                        push rax
                    
                    addr_3:
                
                        ;; pushing 97 to the stack
                        push 97

                
                    addr_4:
                
                        ;; handling write to mem operation
                        pop rbx
                        pop rax
                        mov [rax], bl
                    
                    addr_5:
                
                        ;; pushing 1 to the stack
                        push 1

                
                    addr_6:
                
                        push mem
                    
                    addr_7:
                
                        ;; pushing 1 to the stack
                        push 1

                
                    addr_8:
                
                        ;; pushing 1 to the stack
                        push 1

                
                    addr_9:
                
                        ;; performing a syscall
                        pop rax ;; syscall code
                        pop rdi
                        pop rsi
                        pop rdx
                        syscall
                    

                    mov rax, 60
                    mov rdi, 0
                    syscall
            