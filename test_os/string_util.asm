#once
#include "cpu_def.asm"



PrintString:
	; A holds a pointer to the C style string to print
	push A
	push B
	_PrintSTART:
	lb B, A, 0
	cmpu B, ZERO
	bchi EQUAL, _PrintFinish
	sb B, ZERO, 0xc0000000
	add A, ONE, A
	jmp _PrintSTART
	_PrintFinish:
		pop B
		pop A
		rtn
