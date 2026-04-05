#once
#include "cpu_def.asm"
#include "mem_map.asm"
#include "string_util.asm"
#include "utils.asm"
#include "stack.asm"


main:
	
	limd A, CheckingMBRIntegerty
	call PrintString
	
	sw ZERO, ZERO, HDD_LBA
	lb ZERO, ZERO, HDD_WR
	lh A, ZERO, HDD_BLOCK_START + 510
	
	limd B, 0xAA55
	
	cmpu A, B
	bchi EQUAL, _MBR_OK
	limd A, FAILEDResponse
	call PrintString
	limd A, CheckFailedHalting
	call PrintString
	halt
	
	_MBR_OK:
		limd A, PASSEDResponse
		call PrintString
		limd A, SearchBootPartition
		call PrintString
		
		
		limd A, HDD_BLOCK_START + 446
		and Y, A, A
		call checkParititon
		cmpu A, ZERO
		bchi EQUAL, _partFound
		
		limd A, HDD_BLOCK_START + 446+16
		and Y, A, A
		call checkParititon
		cmpu A, ZERO
		bchi EQUAL, _partFound
		
		limd A, HDD_BLOCK_START + 446+32
		and Y, A, A
		call checkParititon
		cmpu A, ZERO
		bchi EQUAL, _partFound
		
		limd A, HDD_BLOCK_START + 446 + 48
		and Y, A, A
		call checkParititon
		cmpu A, ZERO
		bchi EQUAL, _partFound
		
		limd A, NoBootPartitionFound
		call PrintString
		halt
		
		
		_partFound:
			limd A, FoundParitionAt
			
			call PrintString
			
		
			lw A, Y, 8 ; Load LBA
			
			call PrintInt
			
			and Y, A, A
			
			sw A, ZERO, HDD_LBA
			
			limd A, 10
			
			sb A, ZERO, SERIAL_DATA
			
			
			lb ZERO, ZERO, HDD_WR
			
			sw Y, ZERO, Partition_LBA_Begin
			limd A, BytesPerSector
			call PrintString
			
			lh B, ZERO, HDD_BLOCK_START + 0x0B ;Bytes per sector
			or A, B, ZERO
			call PrintInt
			sh B, ZERO, BPB_BytsPerSec
			limd A, SectorsPerCluster
			call PrintString
			
			lb B, ZERO, HDD_BLOCK_START + 0x0D ; Sectors per Cluster
			or A, B, ZERO
			call PrintInt
			
			sh B, ZERO, sectors_per_cluster
			lh C, ZERO, HDD_BLOCK_START + 0x0E ;Resereved Sectors
			sh C, ZERO, BPB_RsvdSecCnt
			lb D, ZERO, HDD_BLOCK_START + 0x10 ; Number of Fats
			sb D, ZERO, BPB_NumFATs
			lw E, ZERO, HDD_BLOCK_START + 0x24 ; Sectors Per Fat
			sw E, ZERO, Sectors_Per_FAT
			limd A, SectorsPerFAT
			call PrintString
			or A, E, ZERO
			call PrintInt
			
			lw B, ZERO, HDD_BLOCK_START + 0x2C ; Root Directory First Cluster
			sw B, ZERO, root_dir_first_cluster
			
			
			limd A, 10
			sb A, ZERO, SERIAL_DATA

			sw C, ZERO, fat_begin_lba
			mul V, D, E
			add V, V, C ;cluster_begin_lba
			sw V, ZERO, cluster_begin_lba

			
			limd A, FATBeginLBA
			call PrintString
			or A, F, ZERO
			call PrintInt
			
						
			limd A, ClusterBeginLBA
			call PrintString
			or A, V, ZERO
			call PrintInt
			
			
			call findKernelFile
			
			call loadKernelAndRun
			
			
			halt
			

findKernelFile:
	push RA
	push B
	push C ; Stores the entry address
	
				
	limd A, ReadingRootDirectory
	call PrintString
			
	
	lw A, ZERO, root_dir_first_cluster ; Load root DIR first cluster
	call loadCluster
			
	limd A, LoadedCluster
	call PrintString
			

	limd A, SearchingForKernel
	call PrintString
			
	limd A, FAT_CLUSTER
	
	_findKernelFile_checkEntryType:
		OR C, A, A
		call checkFAT32DirectoryTableEntry
		
		limd B, 3
		cmpu B, A
		bchi EQUAL, _findKernelFile_EndOfDIR
		
		cmpu ONE, A
		bchi EQUAL, _findKernelFile_foundFile
		
		limd B, 32
		add A, B, C
		
		jmp _findKernelFile_checkEntryType
		
		_findKernelFile_foundFile:
			
			limd A, FoundFile
			call PrintString
			
			or A, C, C
			call PrintFileNameString
			
			limd B, FileName
			or A, C, C
			call CMPFileNameStrings
			
			

			cmpu A, ZERO
			bchi EQUAL, _findKernelFile_FoundKernel 
			
			limd B, 32
			add A, B, C
			
			jmp _findKernelFile_checkEntryType



	_findKernelFile_EndOfDIR:
		limd A, NoKernelFound
		call PrintString
		halt
		
	_findKernelFile_FoundKernel:
		limd A, KernelFoundMsg
		call PrintString
		
		or A, C, C
	

	pop C
	pop B
	pop RA
	rtn


loadKernelAndRun:
	
	push RA
	push B ;ClusterNumder
	push C ;Size
	push D
	push E
	push F

	
	
	lh B, A, 0x14
	lh C, A, 0x1A
	
	limd D, 65536
	mul B, B, D
	add B, C, B
		
	lw D, A, 0x1C
	
	
	
	or A, B, B
	call PrintInt
	
	limd E, 10
	sb E, ZERO, SERIAL_DATA
	
	or A, D, D
	call PrintInt
	
	limd E, 512
	lh F, ZERO, sectors_per_cluster
	mul E, F, E ;Get Bytes per cluster
	
	cmpu E, D
	bchi GREATER, _loadKernelAndRun_SingleClusterFile ;boot.bin is only a single cluster!
	
	limd A, LargeKernel
	call PrintString
	
	halt
	
	_loadKernelAndRun_SingleClusterFile:
		
	or A, B, B
	
	
	call loadCluster
	
	or A, ZERO, ZERO
	or B, ZERO, ZERO
	or C, ZERO, ZERO
	or D, ZERO, ZERO
	or E, ZERO, ZERO
	or F, ZERO, ZERO
	or G, ZERO, ZERO
	or H, ZERO, ZERO
	or I, ZERO, ZERO
	or J, ZERO, ZERO
	or K, ZERO, ZERO
	or L, ZERO, ZERO
	or M, ZERO, ZERO
	or N, ZERO, ZERO
	or O, ZERO, ZERO
	or P, ZERO, ZERO
	or Q, ZERO, ZERO
	or R, ZERO, ZERO
	or S, ZERO, ZERO
	or T, ZERO, ZERO
	or U, ZERO, ZERO
	or V, ZERO, ZERO
	or W, ZERO, ZERO
	or X, ZERO, ZERO
	or Y, ZERO, ZERO
	or Z, ZERO, ZERO
	or SCRATCH1, ZERO, ZERO
	or RA, ZERO, ZERO
	or STATUS, ZERO, ZERO
	
	;jmp FAT_CLUSTER + 16
	
	limd A, FAT_CLUSTER
	
	call dumpSector512
	
	halt

LargeKernel:
#d "Multi Cluster Kernel Detected! Halting! \n \0"


loadCluster:
	; A holds the cluster number to load
	
	push RA
	push A
	push B ; RAM Block start
	push C ; Sectors left to copy
	push D ; sector size
	push E ; LBA
	push F
	push G
	push H
	
	or B, A, ZERO ; Save A really quick to use A for this print Call
	
	limd A, LoadingCluster
	
	call PrintString
	
	or A, B, ZERO
	
	call PrintInt ; Print out the cluster we are loading
	
	limd B, 10
	
	sb B, ZERO, SERIAL_DATA ; Send a new line char
	
	
	
	call calc_cluster_lba_start ; Convert Cluster num to start LBA
	
	or E, A, ZERO ; Save the LBA into E since we need to use A for func calls
	
	
	lh C, ZERO, sectors_per_cluster ; Get sectors per cluster
	sub C, C, ONE ; Subtract one since we are block copying one before the loop
	
	sw E, ZERO, HDD_LBA ; Load LBA into drive
	lb ZERO, ZERO, HDD_WR ; Load the sector into drive's block
	
	limd B, FAT_CLUSTER ; FAT Ram loc
	limd D, 512
		
	limd G, CopyingSector ; Load String pointer into G since we reuse it over and over
	
	limd H, ForCluser ; Load String pointer into G since we reuse it over and over
	
	or A, G, ZERO
	
	call PrintString
	
	or A, E, ZERO
	
	call PrintInt
	
	or A, H, ZERO
	
	call PrintString
	
	limd A, HDD_BLOCK_START
	
	call BlockCopy512
	
	
	
	
	_copyClusterloop:
		cmpu C, ZERO
		bchi EQUAL, __copyClusterloopdone
		add E, ONE, E ; Incerment LBA
		add B, D, B ; Offset ram addr by 512
		sw E, ZERO, HDD_LBA ; Reload Drive block
		lb ZERO, ZERO, HDD_WR
		
		or F, A, ZERO
		
		or A, G, ZERO
	
		call PrintString
		
		or A, E, ZERO
		
		call PrintInt
		
		or A, H, ZERO
		
		call PrintString
		
		or A, F, ZERO
		
		call BlockCopy512
		sub C, C, ONE
		jmp _copyClusterloop

	__copyClusterloopdone:
		pop H
		pop G
		pop F
		pop E
		pop D
		pop C
		pop B
		pop A
		pop RA
		rtn

getDirectoryEntryFirstCluster:
	; A Address to entry
	lw A, A, 0x14
	rtn

checkFAT32DirectoryTableEntry:
	; A Address to entry start
	; Returns 0 for invalid (Unused / Long Name) entries
	; Returns 1 if the directory entry is for a file
	; Returns 2 if the directory entry is for a folder
	; Returns 3 if the entry is End of Directory
	push RA
	push B 
	push C
	push D 
	
	lb B, A, 0 ; Load first byte of entry
	
	cmpu B, ZERO
	bchi EQUAL, _checkFAT32DirectoryTableEntry_EOD
	
	; Check if unused
	
	limd C, 0xE5
	
	cmpu B, C
	bchi EQUAL, _checkFAT32DirectoryTableEntry_Unused
	
	lb B, A, 0x0B ; Load attrib byte
	
	; Check if long Name entry
	
	limd C, 0x0f
	
	and D, B, C
	cmpu D, C

	bchi EQUAL, _checkFAT32DirectoryTableEntry_Unused
	
	limd C, 0x08
	
	and D, B, C
	cmpu D, C

	bchi EQUAL, _checkFAT32DirectoryTableEntry_Unused
	
	limd C, 0x10
	and D, B, C
	cmpu D, C
	
	bchi EQUAL, _checkFAT32DirectoryTableEntry_DIR
	
	limd A, 1
	jmp _checkFAT32DirectoryTableEntry_end
	
	_checkFAT32DirectoryTableEntry_DIR:
		limd A, 2
		jmp _checkFAT32DirectoryTableEntry_end
	
	_checkFAT32DirectoryTableEntry_Unused:
		limd A, 0
		jmp _checkFAT32DirectoryTableEntry_end
	
	_checkFAT32DirectoryTableEntry_EOD:
		limd A, 3
	
	_checkFAT32DirectoryTableEntry_end:
		pop D
		pop C
		pop B
		pop RA
		rtn
			
		
checkParititon:
	; A Address to entry start; Returns A
	push RA
	push B
	push C
	
	limd C, 0x80
	
	lb B, A, 0
	
	cmpu B, C
	bchi EQUAL, _okay
	and A, ONE, ONE
	rtn
	
	_okay:
	lb B, A, 4
	limd C, 0x0B
	cmpu B, C
	bchi EQUAL, _okay2
	limd C, 0x0C
	cmpu B, C
	bchi EQUAL, _okay2
	limd C, 0x1B
	cmpu B, C
	bchi EQUAL, _okay2
	limd C, 0x1C
	cmpu B, C
	bchi EQUAL, _okay2
	and A, ONE, ONE
	pop C
	pop B
	pop RA
	rtn
	
	_okay2:
	and A, ZERO, ZERO
	pop C
	pop B
	pop RA
	rtn
	
	
calc_cluster_lba_start:
	; A is cluster number
	; Returns LBA in A
	push B
	sub A, A, ONE
	sub A, A, ONE
	lb B, ZERO, sectors_per_cluster
	mul A, A, B
	lw B, ZERO, cluster_begin_lba
	add A, B, A
	lw B, ZERO, Partition_LBA_Begin
	add A, B, A
	pop B
	rtn

	
CheckingMBRIntegerty:
#d "Checking MBR Integerty... \0"
	
FAILEDResponse:
#d "Failed!\n\0"

CheckFailedHalting:
#d "Check Failed. Halting! \n\0"

PASSEDResponse:
#d "PASSED! \n\0"

CopyingSector:
#d "\nCopying Sector \0"

ForCluser:
#d " for a cluster\n\0"
	
LoadedCluster:
#d "Loaded Cluster\n\0"

LoadingCluster:
#d "Loading Cluster \0"
		
	
	
FoundParitionAt:
#d "Found bootable FAT32 partition @ \0"	
	
SearchBootPartition:
#d "Searching for bootable partition.\n\0"

NoBootPartitionFound:
#d "No bootable parition found! Halting. \0"

ReadingRootDirectory:
#d "\nReading root directory...\n\0"

SearchingForKernel:
#d "Searching for BOOT.BIN...\n\0"

KernelFoundMsg:
#d "\nKernel found! Loading...\n\0"

NoKernelFound:
#d "BOOT.BIN not found! Halting.\n\0"

FileName:
#d "BOOT    BIN"

FoundFile:
#d "Found a file entry! Its name is: \0"

KernelLoadedMsg:
#d "Kernel loaded! Jumping to kernel...\n\0"

LoadErrorMsg:
#d "Error loading file! Halting.\n\0"

BytesPerSector:
#d "Bytes per sector \0"

SectorsPerCluster:
#d "\nSectors per Cluster \0"

RootDirectoryFirstCluster:
#d "\nRoot Directory First Cluster \0"

SectorsPerFAT:
#d "\nSectors per FAT \0"

FATBeginLBA:
#d "\nFAT Begin LBA \0"

ClusterBeginLBA:
#d "\nCluster Begin LBA \0"