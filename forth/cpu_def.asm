#once
#subruledef register
{
   ZERO => 0
   ONE  => 1
   
   A => 2
   B => 3
   C => 4
   D => 5
   E  => 6
   F  => 7
   G  => 8
   H  => 9
   I  => 10
   J  => 11
   K  => 12
   L  => 13
   M  => 14
   N  => 15
   O  => 16
   P  => 17
   Q  => 18
   R  => 19
   S  => 20
   T  => 21
   U  => 22
   V  => 23
   W  => 24
   X  => 25
   Y  => 26
   Z  => 27
   SCRATCH1 => 28 ; Just needed a name for this register since I used up all the letters. 
   RA => 29 ; Return Address
   STATUS => 30 ; Status 
   INT_RA => 31 ; Intrrupt Return, sort of useless if outside an interrupt with them enabled, if they are disable could use as random register
   
}

#subruledef condition
{
	UNCONDITIONAL => 0
	CARRY8 => 1
	CARRY16 => 2
	CARRY32 => 4
	ZERO => 8
	GREATER => 16
	EQUAL => 32
	
}

#ruledef
{
	
	;rd is register where the result of the instruction will be stored
	;r1 is first parm
	;r2 is second parm
	
    NOP  => 0x00 @ 0x00 @ 0x00 @ 0x00 ;NOP
	lw {rd: register}, {r1: register}, {addr: u32} => le(0x1`5 @ rd`5 @ r1`5 @ 0x0`17) @  le(addr`32) ;Load Word (32-bit), r1 is register containing an offset added to the addr
	lh {rd: register}, {r1: register}, {addr: u32} => le(0x2`5 @ rd`5 @ r1`5 @ 0x0`17) @  le(addr`32) ;Load Half Word (16-bit) , r1 is register containing an offset added to the addr
	lb {rd: register}, {r1: register}, {addr: u32} => le(0x3`5 @ rd`5 @ r1`5 @ 0x0`17) @  le(addr`32) ;Load Byte (8-bit), r1 is register containing an offset added to the addr
	
	sw {r2: register}, {r1: register}, {addr: u32} => le(0x4`5 @ 0x0`5 @ r1`5 @ r2`5 @ 0x0`12) @ le(addr`32) ;Store Word (32-bit), r1 is register containing an offset added to the addr, r2 is register being stored
	sh {r2: register}, {r1: register}, {addr: u32} => le(0x5`5 @ 0x0`5 @r1`5 @ r2`5 @ 0x0`12) @  le(addr`32) ;Store Half Word (16-bit), r1 is register containing an offset added to the addr, r2 is register being stored
	sb {r2: register}, {r1: register}, {addr: u32} => le(0x6`5 @ 0x0`5 @ r1`5 @ r2`5 @ 0x0`12) @  le(addr`32) ;Store Byte (8-bit), r1 is register containing an offset added to the addr, r2 is register being stored
	
	sexth {rd: register}, {r1: register} => le(0x7`5 @ rd`5 @ r1`5 @ 0x0`17) ; Sign-extend Half Word to Word
	sextb {rd: register}, {r1: register} => le(0x8`5 @ rd`5 @ r1`5 @ 0x0`17) ;Sign-extend Byte to Word
	
	limd  {rd: register}, {value: u32} => le(0x9`5 @ rd`5 @ 0x0`5 @ 0x0`17) @ le(value`32) ;Load Immd 

	add  {rd: register}, {r1: register}, {r2: register} => le(0xA`5 @ rd`5 @ r1`5 @ r2`5 @ 0x0`12) ;ADD
	sub {rd: register}, {r1: register}, {r2: register} => le(0xB`5 @ rd`5 @ r1`5 @ r2`5 @ 0x0`12) ;SUB
	mul {rd: register}, {r1: register}, {r2: register} => le(0xC`5 @ rd`5 @ r1`5 @ r2`5 @ 0x0`12) ;MULTIPLY
	div {rd: register}, {r1: register}, {r2: register} => le(0xD`5 @ rd`5 @ r1`5 @ r2`5 @ 0x0`12) ;DIVIDE
	shl {rd: register}, {r1: register} => le(0xE`5 @ rd`5 @ r1`5 @ 0x0`5 @ 0x0`12) ;SHIFT LEFT 1
	shr {rd: register}, {r1: register} => le(0xF`5 @ rd`5  @ r1`5 @ 0x0`5 @ 0x0`12) ;SHIFT RIGHT 1
	and {rd: register}, {r1: register}, {r2: register} => le(0x10`5 @ rd`5 @ r1`5 @ r2`5 @ 0x0`12) ;AND
	or {rd: register}, {r1: register}, {r2: register} => le(0x11`5 @ rd`5 @ r1`5 @ r2`5 @ 0x0`12) ;OR
	xor {rd: register}, {r1: register}, {r2: register} => le(0x12`5 @ rd`5 @ r1`5 @ r2`5 @ 0x0`12) ;XOR
	not {rd: register}, {r1: register} => le(0x13`5 @ rd`5 @ r1`5 @ 0x0`5 @ 0x0`12) ;NOT
	
	cmps {r1: register}, {r2: register} => le(0x14`5 @0x0`5 @ r1`5 @ r2`5 @ 0x0`12) ;compare signed result stored in STATUS register
	cmpu {r1: register}, {r2: register} => le(0x15`5 @0x0`5 @ r1`5 @ r2`5 @ 0x0`12) ;compare unsigned result stored in STATUS register
	
	bchi {c: condition}, {addr: u32} =>  le(0x16`5 @ 0x0`5 @ 0x0`5 @ 0x0`5 @ c`8 @ 0x0`4 ) @ le(addr`32) ;branch based off STATUS register branchs to address
	bchr {c: condition}, {r1: register} =>  le(0x17`5 @0x0`5 @ r1`5 @ 0x0`5 @ 0x0`5 @ c`8 @ 0x0`4 ) ;branch based off STATUS register to address in r1
	
	call {addr: u32} => le(0x18`5 @0x0`5 @ 0x0`5 @ 0x0`5 @ 0x0`12)@ le(addr`32) ;Call subrutine at addr
	callr {r1: register} => le(0x19`5 @0x0`5 @ r1`5 @ 0x0`17) ;Call subrutine at address in r1
	rtn => le(0x1A`5 @0x0`5 @ 0x0`5 @ 0x0`17) ;return from subrutine to address in RA
	
	wctl {r2: register}, {r1: register} => le(0x1B`5 @ 0`5 @ r1`5 @ r2`5 @ 0x0`12) ;write control register  r1 is register addr, r2 is word to write
	rctl {rd: register}, {r1: register}  => le(0x1C`5 @ rd`5 @ r1`5 @ 0x0`17) ;read control register r1 is register addr, r2 is word to read

	aswap {rd: register}, {r1: register}, {addr: u32} => le(0x1D`5 @ rd`5 @ r1`5 @ 0x0`17) @ le(addr`32) ;atomic swap - Reads addr into rd and stores r1 into addr 

	syscall {r1: register} => le(0x1E`5 @ 0x0`5 @ r1`5 @ 0x0`17) ; software interrupt
	sysrtn => le(0x1F @ 0x00 @ 0x00 @ 0x00) ;return interrup


	halt => asm
	{_halt:
	bchi UNCONDITIONAL, _halt
	}
	
	jmp {addr} => asm
	{
	bchi UNCONDITIONAL, {addr}
	}

}


jmp main