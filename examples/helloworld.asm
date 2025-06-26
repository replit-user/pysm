mov ar1, "Hello, World!\n" ;move the string Hello, World!
;into ar1
mov scr, 10 ;print syscall number
sys ;invoke the syscall
mov frr, 0 ;move the value 0 to frr
mov scr, 20 ;exit syscall
sys ;preform the syscall
