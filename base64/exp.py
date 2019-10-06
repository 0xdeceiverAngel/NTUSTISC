from pwn import *
import base64
context(os='linux',arch='amd64',log_level='debug')
r=remote("isc.taiwan-te.ch",10801)
rec=r.recvline()
rec=r.recvline()
rec=r.recvline()
rec=r.recvline()
ans=""
for i in range(100):
    r.recvline()
    rec=r.recvline()
    rec=str(base64.b64decode(rec))
    r.recv()
    rec=str(rec.split('=')[0])
    ans+=(chr(eval(rec)))
    # print eval(rec)
    r.sendline(str(eval(rec)))
print ''.join(ans)
print base64.b64decode(ans)
r.interactive()


# 44GK55ay44KM5qeY
# flag{base64 is tooooooo eeeeaaasy, but sorry this issssss mmmisccc XDDDDD}
