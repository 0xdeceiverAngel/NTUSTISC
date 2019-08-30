# lab4 gothijack

這一題很明顯題目就告訴你了

首先 name 裡要塞 shellcode

addr 寫入 要修改的addr

然後 再寫入要修改的內容

這樣就行了

因為是got劫持

因為後面有個puts 所以我們劫持puts

讓它call puts 時 會call 我們的shellcode

```=
[*] '/home/user/Downloads/ntus/Lab 4/gothijack'
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX disabled
    PIE:      No PIE (0x400000)
    RWX:      Has RWX segments
```
很好NX 沒開 可以填shellcode
```=
[0x00400717]> s sym.imp.puts
[0x004005d0]> pdf
/ (fcn) sym.imp.puts 6
|   sym.imp.puts (const char *s);
|           ; CALL XREFS from sym.main (0x400771, 0x400793, 0x4007de)
\           0x004005d0      ff25420a2000   jmp qword reloc.puts        ; [0x601018:8]=0x4005d6

```
puts 的 got 位置是 0x601018

或是要寫 printf 也可以

```=
  0x0040076a      488d3d330100.  lea rdi, qword str.What_s_you_name ; 0x4008a4 ; "What's you name?"
| 0x00400771      e85afeffff     call sym.imp.puts           ; int puts(const char *s)
| 0x00400776      ba40000000     mov edx, 0x40               ; '@' ; 64
| 0x0040077b      488d35fe0820.  lea rsi, qword obj.name     ; 0x601080
| 0x00400782      bf00000000     mov edi, 0
| 0x00400787      e874feffff     call sym.imp.read           ; ssize_t read(int fildes, void *buf, size_t nbyte)
```
name 的位置是 0x601080
