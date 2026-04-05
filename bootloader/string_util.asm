#once
#include "cpu_def.asm"
#include "mem_map.asm"


PrintString:
	; A holds a pointer to the C style string to print
	push A
	push B
	_PrintSTART:
	lb B, A, 0
	cmpu B, ZERO
	bchi EQUAL, _PrintFinish
	sb B, ZERO, SERIAL_DATA
	add A, ONE, A
	jmp _PrintSTART
	_PrintFinish:
		pop B
		pop A
		rtn

PrintFileNameString:
	; A holds a pointer to the FAT32 name
	push B
	lb B, A, 0
	sb B, ZERO, SERIAL_DATA
	lb B, A, 1
	sb B, ZERO, SERIAL_DATA
	lb B, A, 2
	sb B, ZERO, SERIAL_DATA
	lb B, A, 3
	sb B, ZERO, SERIAL_DATA
	lb B, A, 4
	sb B, ZERO, SERIAL_DATA
	lb B, A, 5
	sb B, ZERO, SERIAL_DATA
	lb B, A, 6
	sb B, ZERO, SERIAL_DATA
	lb B, A, 7
	sb B, ZERO, SERIAL_DATA
	lb B, A, 8
	sb B, ZERO, SERIAL_DATA
	lb B, A, 9
	sb B, ZERO, SERIAL_DATA
	lb B, A, 10
	sb B, ZERO, SERIAL_DATA
	limd B, 10
	sb B, ZERO, SERIAL_DATA
	pop B
	rtn
	
CMPFileNameStrings:
	; A holds a pointer to the FAT32 name
	; B holds a pointer to the FAT32 name
	; Returns 0 for good and 1 for no match
	push B
	push C
	push D
	push E
	push F
	limd F, 10
	limd E, 0
	
	_CMPFileNameStrings_loop:
	cmpu E, F
	bchi EQUAL, _CMPFileNameStrings_exit_good
	add A, ONE, A
	add B, ONE, B
	lb C, A, 0
	lb D, B, 0
	cmpu C, D
	add E, ONE, E
	bchi EQUAL, _CMPFileNameStrings_loop
	limd A, 1
	jmp _CMPFileNameStrings_exit
	
	
	_CMPFileNameStrings_exit_good:
		limd A, 0
		
	_CMPFileNameStrings_exit:
	pop F
	pop E
	pop D
	pop C
	pop B
	rtn
		
		
PrintInt:
	; A holds the int to print
	push A
	push B
	push C
	push D
	push E
	push F
	push RA
	
	limd B, 10
	limd C, 11
	limd F, 48
	cmpu A, ZERO
	bchi EQUAL, _printZero
	
	sb ZERO, ZERO, PrintIntBufferEnd	
	_PrintIntLoop:
	cmpu A, ZERO
	bchi EQUAL, _PrintIntDone
	
	div D, A, B
	mul D, B, D
	
	sub D, A, D
	
	add D, F, D
	
	sb D, C, PrintIntBuffer
	
	sub C, C, ONE
	
	div A, A, B
	
	jmp _PrintIntLoop
	
	_printZero:
	
	add A, F, A 
	sb A, ZERO, SERIAL_DATA
		
	jmp _PrintIntExit
	
	_PrintIntDone:
	limd A, PrintIntBuffer
	add A, C, A
	add A, A, ONE
	
	call PrintString
	
	_PrintIntExit:
	
	pop RA
	pop F
	pop E
	pop D
	pop C
	pop B
	pop A
	rtn
			
StringCMP:
	; A holds points to first string
	; B holds points to second string
	;Clobers C and D
	lb C, A, 0
	lb D, B, 0
	cmpu C, D
	bchi EQUAL, _CMP_Equal
	jmp _NotEqual
	_CMP_Equal:
	cmpu C, ZERO
	bchi EQUAL, _CMPEqualFinish
	add A, ONE, A
	add B, ONE, B
	jmp StringCMP
	_CMPEqualFinish:
		and A, ZERO, ZERO
	
	_NotEqual:
		and A, ONE, ONE
		
	rtn
	

dumpSector512:
	push RA
	push B
	push C
	
	limd C, 512
	or B, A, A
	dumpSector512_loop:
		

		lb A, B, 0
		
		call PrintInt
		
		limd A, 44
		sb A, ZERO, SERIAL_DATA
		
		add B, B, ONE
		sub C, C, ONE
		
		cmpu C, ZERO
		bchi EQUAL, dumpSector512_exit
		
		jmp dumpSector512_loop
	
	dumpSector512_exit:
	pop C
	pop B
	pop RA
	rtn