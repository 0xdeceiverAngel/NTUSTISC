from pwn import*
context(os='linux',arch='i386',log_level='debug')
#n = process('./rop')

n=remote('isc.taiwan-te.ch',9999)


n.recvuntil('\n')
n.sendline(p32(0xdeadbeef))
n.recvuntil('\n')
for i in range(1000):
	s=n.recvuntil('?')
	a=s.split(' ')[0]
	b=s.split(' ')[1]
	c=s.split(' ')[2]
	if(b=='+'):
		q=int(a)+int(c)
		n.sendline(str(q))
	if(b=='-'):
		q=int(a)-int(c)
		n.sendline(str(q))
	if(b=='*'):
		q=int(a)*int(c)
		n.sendline(str(q))
	if(s=='Good job!\n'):
		break


n.interactive()


#FLAG{pwn70015_15_c0nv3n13n7}

