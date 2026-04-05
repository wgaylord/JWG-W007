#once
#include "cpu_def.asm"	
#const STACK_START = 16384	

#ruledef
{
    push {reg: register} => asm { 
	sw {reg}, Z, STACK_START
	limd SCRATCH1, 4
	add Z, SCRATCH1, Z
	}
	
	pop {reg: register} => asm {
	limd SCRATCH1, 4
	sub Z, Z, SCRATCH1
	lw {reg}, Z, STACK_START
	}
	
	peek {reg: register} => asm {
		limd SCRATCH1, 4
		sub Z, Z, SCRATCH1
		lw {reg}, Z, STACK_START
		add Z, SCRATCH1, Z
	}
}