#once
#include "cpu_def.asm"
#include "mem_map.asm"


InitInputData:
	limd SCRATCH1, 0
	sb SCRATCH1, ZERO, STRING_BUFFER_POINTER
	rtn


InputRoutine:
	sw A, Z, CPU_STACK
	limd SCRATCH1, 4
	add Z, SCRATCH1, Z
	sw B, Z, CPU_STACK
	add Z, SCRATCH1, Z
	sw STATUS, Z, CPU_STACK
	add Z, SCRATCH1, Z
	
	
	lb B, ZERO, STRING_BUFFER_POINTER
	lb A, ZERO, SERIAL_DATA	
	
	cmpu A, ZERO
	bchi EQUAL, InputRoutineExit
	
	sb A, B, STRING_BUFFER
	sb A, ZERO, SERIAL_DATA
	add B, ONE, B
	sb B, ZERO, STRING_BUFFER_POINTER
	
	InputRoutineExit:
	
	limd SCRATCH1, 4
	sub Z, SCRATCH1, Z
	lw STATUS, Z, CPU_STACK
	sub Z, SCRATCH1, Z
	lw B, Z, CPU_STACK
	sub Z, SCRATCH1, Z
	lw A, Z, CPU_STACK
	rtn
	