#once
#include "cpu_def.asm"	


#ruledef
{
	init_stack {addr: u32} => asm { 
		limd z, {addr}
	}
	
    push {reg: register} => asm { 
	sw {reg}, Z, 0
	limd SCRATCH1, 4
	sub Z, SCRATCH1, Z
	}
	
	pop {reg: register} => asm {
	limd SCRATCH1, 4
	add Z, Z, SCRATCH1
	lw {reg}, Z, 0
	}
	
	peek {reg: register} => asm {
		limd SCRATCH1, 4
		add Z, Z, SCRATCH1
		lw {reg}, Z, 0
		sub Z, SCRATCH1, Z
	}
}