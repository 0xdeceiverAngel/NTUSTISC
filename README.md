# lab 3
```=
   Arch:     amd64-64-little
   RELRO:    Partial RELRO
   Stack:    No canary found
   NX:       NX disabled
   PIE:      No PIE (0x400000)
   RWX:      Has RWX segments

```
保護都關 RWX 有開 用`seccomp-tools`看

如果沒有擋 它會幫你把程式跑起來 這題沒有擋

code 裡沒有寫好的 shell

所以要自己搞shell

https://www.exploit-db.com/shellcodes

第一個輸入寫入shellcode 不能超過48byte

第二個輸入讓它bof 跳回shellcode的位置

至於位置怎麼找 用gdb下去追
