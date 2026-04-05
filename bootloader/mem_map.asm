#once
#const SERIAL_DATA = 0xc0000000
#const RAM_START = 8192
#const HDD_LBA = 0xc0000400
#const HDD_WR = 0xc0000404
#const HDD_BLOCK_START = 0xc0000408
#const HDD_BLOCK_SIZE = 0x200



#const PrintIntBuffer = RAM_START
#const PrintIntBufferEnd = RAM_START + 12


#const MBR_VALIDATION_BYTES = HDD_LBA + 510

#const Partition_LBA_Begin = RAM_START + 1024
#const BPB_BytsPerSec = Partition_LBA_Begin + 4
#const sectors_per_cluster = BPB_BytsPerSec + 2
#const BPB_RsvdSecCnt = sectors_per_cluster + 2
#const BPB_NumFATs = BPB_RsvdSecCnt + 2
#const Sectors_Per_FAT = BPB_NumFATs + 2
#const root_dir_first_cluster = Sectors_Per_FAT + 4
#const fat_begin_lba = root_dir_first_cluster + 4
#const cluster_begin_lba = fat_begin_lba + 4


#const FAT_CLUSTER = RAM_START + 2048



