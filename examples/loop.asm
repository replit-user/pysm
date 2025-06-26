mov r1,0 ;mov 0 into r1
loop:
inc r1 ;increment r1 by 1 
mov scr,10; print
mov ar1,r1 ;move the value in r1 to ar1
sys ;outputs the value in ar1(syscall)
mov ar1,"\n" ;newline
sys ;syscall
jl loop ;jump to loop 'label' more of a function
ret ;end label
jl loop ;call the loop function