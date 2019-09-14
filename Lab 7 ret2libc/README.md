# lab 7 ret2libc
stack GOT ...and so on, can leak libc
- 先用objdump 找 puts GOT 然後 leak 位置
- 用readelf -a libc.so 找puts初始位置
- 算 offset
- 找sh字串位置 strings libc.so -tx |grep "/bin/sh"
- ROPgadget --binary libc.so>list 找gadget
- ROP疊一疊 就可以

-或用 one_gadget libc.so
## futher more
- stack migration 自己造stack
