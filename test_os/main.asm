#once
#bankdef mybank
{
    bits = 8
    addr = 10240
    size = 262144
    outp = 8 * 0x10
}
#bank mybank
#include "cpu_def.asm"

main:
	
	limd A, Test
	call PrintString
	halt

Test:
#d "BOOTED Test kernel!\n\0"

#include "string_util.asm"
#include "stack.asm"