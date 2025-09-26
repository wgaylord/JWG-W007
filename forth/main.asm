#once
#include "cpu_def.asm"
#include "mem_map.asm"
#include "string_buffer.asm"


main:

call InitInputData


MainLoop:
	call InputRoutine
	jmp MainLoop
