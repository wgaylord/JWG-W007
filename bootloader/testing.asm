#once
#include "cpu_def.asm"
#include "mem_map.asm"
#include "string_util.asm"
#include "utils.asm"
#include "stack.asm"


main:
	
	limd B, 10
	
	limd A, TestingPrintInt
	call PrintString
	
	limd A, 1
	
	call PrintInt
	
	sb B, ZERO, SERIAL_DATA
	
	limd A, TestingPrintSerialAddreess
	call PrintString
	
	limd A, SERIAL_DATA
	
	call PrintInt

	sb B, ZERO, SERIAL_DATA
	
	halt


TestingPrintInt:
#d "Testing Print 1\n\0"
	
	
TestingPrintSerialAddreess:
#d "Testing Print Serial Address 3221225472 \n\0"