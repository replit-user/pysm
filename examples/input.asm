print:
mov scr,10 ;print syscall
sys ;invoke the syscall
ret ;return
input:
mov scr,15 ;input syscall
sys ;invoke syscall
ret ;return
mov ar1,"what is your name:\t" ;prompt
jl input ;jump to input
mov r1,frr ;move the result of the input to r1
mov ar1,"Hello, " ;move the string Hello,  into ar1
jl print ;jumps to the print label
mov ar1,r1 ;move the input output to ar1
jl print ;jump to print again
mov ar1,"!\n" ;move !
;into ar1
jl print ;call print
mov scr,20 ;exit syscall
mov frr,0 ;exit number
sys ;the actual syscall, everything past here is ignored