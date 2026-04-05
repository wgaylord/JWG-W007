#once
#include "cpu_def.asm"
#include "mem_map.asm"
#include "stack.asm"


BlockCopy512:
	; A Pointer of where to copy from
	; B Pointer of where to copy to
	; Clobber C, D, E
	; Src and Dst must be on 4 byte aligned boundary
	push A
	push B
	push C
	push D
	push E
	push F
	push G
	
	and C, ZERO, ZERO
	limd D, 4
	limd E, 128
	limd G, 46
	
	_BlockCopy512loop:
		sb G, ZERO, SERIAL_DATA
		lw F, A, 0
		sw F, B, 0
		add C, C, ONE
		cmpu C, E
		bchi EQUAL, _BlockCopy512done
		add A, D, A
		add B, D, B
		jmp _BlockCopy512loop
		
	_BlockCopy512done:
		pop G
		pop F
		pop E
		pop D
		pop C
		pop B
		pop A
		rtn
		
	
	
