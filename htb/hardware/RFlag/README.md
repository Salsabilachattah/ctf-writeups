# RFlag writeup

## Basic commands
- I started with the file command , tbh i had no clue what the outupu even meant lol :
`file signal.cf32`                                                                                                                                 
`signal.cf32: Adobe Photoshop Color swatch, version 0, 49212 colors; 1st RGB space (0), w 0xc0bc, x 0, y 0x803c, z 0; 2nd space (32956), w 0, x 0xc03c, y 0, z 0xc0bc`
- So then i googled the file extension and found this :
`Complex Float 32-bit`
- So helpful ! I asked perplexity about the tools i can use to read the content of the file and it gave me this tool [rtl-433](https://github.com/merbanan/rtl_433): 
`sudo apt update`
`sudo apt install rtl-433`

- After 5 minutes of trying all options , i read this :
`[-A] Pulse Analyzer. Enable pulse analysis and decode attempt.`

- I ran this command :
`rtl_433 signal.cf32 -A`
`...`
`codes     : {256}2aaaaaaa0c4e4854427b52465f4834636b316e365f31735f6330306c2121217d`
`...`

## Flag
- After decoding the output with cyberchef :
`HTB{RF_H4ck1n6_1s_c00l!!!}`
