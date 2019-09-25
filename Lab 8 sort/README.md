# lab8 sort
```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
全開

~~ var int local_138a8h @ rbp-0x138a8                                           
var int local_138a0h @ rbp-0x138a0                                          
var int local_20h @ rbp-0x20        這是name                                     
var int local_8h @ rbp-0x8          這是canay                                      
arg int arg_138a0h @ rbp+0x138a0   這是arr[]
~~
~~
0x138a0+0x8=0x138a8=80040
80040/8=10005
~~
~~
所以size填106 可以leak canary
~~
***上面全部錯***

## recview
```
; var int local_138b4h @ rbp-0x138b4 //size
; var int local_138b0h @ rbp-0x138b0 // for i
; var int local_138ach @ rbp-0x138ac // for i
; var int local_138a8h @ rbp-0x138a8 // tmp
; var int local_138a0h @ rbp-0x138a0 //array
; var int local_20h @ rbp-0x20       //name   4
; var int local_8h @ rbp-0x8         //canary 1
; arg int arg_138a0h @ rbp+0x138a
; DATA XREF from entry0 (0x7cd)
```
應該是這樣沒錯

之前上面不知道是腦袋撞到還是怎樣 亂亂寫

解了超久 3 的多月 ＝ ＝

因為一開始寫錯 我還懷疑 qsort 有問題 r就跟進去看 跟D能兒一樣

~~
0x000009f9      8b854cc7feff   mov eax, dword [local_138b4h] ;size
0x000009ff      4863f0         movsxd rsi, eax
0x00000a02      488d8560c7fe.  lea rax, qword [local_138a0h];arr[] ptr
0x00000a09      488d0daafeff.  lea rcx, qword [sym.comp]   ; 0x8ba comp()
0x00000a10      ba08000000     mov edx, 8  ;sizeof(long long)
0x00000a15      4889c7         mov rdi, rax ;arr[]  
0x00000a18      e823fdffff     call sym.imp.qsort
rdi  rsi   edx                rcx
arr, size, sizeof(long long), comp
~~
## st1
它一開始 它會問你size 輸入超過10000 可以overflow

然後吃size個數字 你可以輸入小於0 這樣裡面的值就不會被改變

我們要想辦法leak canary 在name塞padload 跳到libc上

當初在leak canary時 搞了超久

因為canary值是隨機

long long int 範圍-2147483648 至 2147483647  2147483647=7FFFFFFF 如果超過它會變成負號

然後它還會sort過再print 所以他有可能在頭或是在尾 如果負號再去處理

再來是找libc 的base address
## st2
pop 第一次 取canary

pop 第二次 ?? 不確定

pop 第三次 libc

因為已經sort過了 所以要依序pop 


rbp 上存著 ` <__libc_start_main+235>:      mov    edi,eax `

利用`objdump -d -Mintel sort> obj_libc`

```
0000000000021ab0 <__libc_start_main@@GLIBC_2.2.5>:
   21ab0:	41 55                	push   r13
   21ab2:	41 54                	push   r12
   21ab4:	31 c0                	xor    eax,eax
   21ab6:	55                   	push   rbp
   21ab7:	53                   	push   rbx
   21ab8:	48 89 cd             	mov    rbp,rcx
   21abb:	48 81 ec 98 00 00 00 	sub    rsp,0x98
   21ac2:	48 89 54 24 08       	mov    QWORD PTR [rsp+0x8],rdx
   21ac7:	48 8b 15 6a 94 3c 00 	mov    rdx,QWORD PTR [rip+0x3c946a]        # 3eaf38 <_dl_starting_up>
   21ace:	48 89 7c 24 18       	mov    QWORD PTR [rsp+0x18],rdi
   21ad3:	89 74 24 14          	mov    DWORD PTR [rsp+0x14],esi
   21ad7:	48 85 d2             	test   rdx,rdx
   21ada:	74 09                	je     21ae5 <__libc_start_main@@GLIBC_2.2.5+0x35>
   21adc:	8b 12                	mov    edx,DWORD PTR [rdx]
   21ade:	31 c0                	xor    eax,eax
   21ae0:	85 d2                	test   edx,edx
   21ae2:	0f 94 c0             	sete   al
   21ae5:	4d 85 c9             	test   r9,r9
   21ae8:	89 05 b2 96 3c 00    	mov    DWORD PTR [rip+0x3c96b2],eax        # 3eb1a0 <h_errlist@@GLIBC_2.2.5+0x1100>
   21aee:	74 0c                	je     21afc <__libc_start_main@@GLIBC_2.2.5+0x4c>
   21af0:	31 d2                	xor    edx,edx
   21af2:	31 f6                	xor    esi,esi
   21af4:	4c 89 cf             	mov    rdi,r9
   21af7:	e8 34 19 02 00       	call   43430 <__cxa_atexit@@GLIBC_2.2.5>
   21afc:	48 8b 15 55 93 3c 00 	mov    rdx,QWORD PTR [rip+0x3c9355]        # 3eae58 <_rtld_global_ro@GLIBC_PRIVATE>
   21b03:	8b 1a                	mov    ebx,DWORD PTR [rdx]
   21b05:	83 e3 02             	and    ebx,0x2
   21b08:	0f 85 da 00 00 00    	jne    21be8 <__libc_start_main@@GLIBC_2.2.5+0x138>
   21b0e:	48 85 ed             	test   rbp,rbp
   21b11:	74 15                	je     21b28 <__libc_start_main@@GLIBC_2.2.5+0x78>
   21b13:	48 8b 05 8e 93 3c 00 	mov    rax,QWORD PTR [rip+0x3c938e]        # 3eaea8 <__environ@@GLIBC_2.2.5-0x31f0>
   21b1a:	48 8b 74 24 08       	mov    rsi,QWORD PTR [rsp+0x8]
   21b1f:	8b 7c 24 14          	mov    edi,DWORD PTR [rsp+0x14]
   21b23:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   21b26:	ff d5                	call   rbp
   21b28:	48 8b 15 29 93 3c 00 	mov    rdx,QWORD PTR [rip+0x3c9329]        # 3eae58 <_rtld_global_ro@GLIBC_PRIVATE>
   21b2f:	8b 82 b0 01 00 00    	mov    eax,DWORD PTR [rdx+0x1b0]
   21b35:	85 c0                	test   eax,eax
   21b37:	0f 85 cb 00 00 00    	jne    21c08 <__libc_start_main@@GLIBC_2.2.5+0x158>
   21b3d:	85 db                	test   ebx,ebx
   21b3f:	0f 85 06 01 00 00    	jne    21c4b <__libc_start_main@@GLIBC_2.2.5+0x19b>
   21b45:	48 8d 7c 24 20       	lea    rdi,[rsp+0x20]
   21b4a:	e8 c1 d0 01 00       	call   3ec10 <_setjmp@@GLIBC_2.2.5>
   21b4f:	85 c0                	test   eax,eax
   21b51:	75 4b                	jne    21b9e <__libc_start_main@@GLIBC_2.2.5+0xee>
   21b53:	64 48 8b 04 25 00 03 	mov    rax,QWORD PTR fs:0x300
   21b5a:	00 00
   21b5c:	48 89 44 24 68       	mov    QWORD PTR [rsp+0x68],rax
   21b61:	64 48 8b 04 25 f8 02 	mov    rax,QWORD PTR fs:0x2f8
   21b68:	00 00
   21b6a:	48 89 44 24 70       	mov    QWORD PTR [rsp+0x70],rax
   21b6f:	48 8d 44 24 20       	lea    rax,[rsp+0x20]
   21b74:	64 48 89 04 25 00 03 	mov    QWORD PTR fs:0x300,rax
   21b7b:	00 00
   21b7d:	48 8b 05 24 93 3c 00 	mov    rax,QWORD PTR [rip+0x3c9324]        # 3eaea8 <__environ@@GLIBC_2.2.5-0x31f0>
   21b84:	48 8b 74 24 08       	mov    rsi,QWORD PTR [rsp+0x8]
   21b89:	8b 7c 24 14          	mov    edi,DWORD PTR [rsp+0x14]
   21b8d:	48 8b 10             	mov    rdx,QWORD PTR [rax]
   21b90:	48 8b 44 24 18       	mov    rax,QWORD PTR [rsp+0x18]
   21b95:	ff d0                	call   rax
   21b97:	89 c7                 	mov    edi,eax

   ... 後面省略
```
找到 mov edi,eax

發現 它在 `__libc_start_main` 裡

跟`__libc_start_main`差了 `21b97` 把它減掉就是 libc base addr

之後就擺上 onegadget
