import mmap

class HDD_RAW_IMG:
    def __init__(self,config):
        print("HDD RAW IMG Device",config)
        self.start = config["start"]
        self.length = config["size"]
        self.file = open(config["binary"],"r+b")
        if config["readonly"]:
            self.memory = mmap.mmap(self.file.fileno(),self.length,access=mmap.ACCESS_READ)
        else:
            self.memory = mmap.mmap(self.file.fileno(),self.length)
        self.LBA = 0
        self.block = self.memory[0:512]
        self.status = 0
        self.command = 0

        
    def read(self,addr,size):
        if not self.isSelected(addr):
            return 0
            
        if size == 1:
            return self.get(addr-self.start)
        elif size == 2 and self.isSelected(addr+1):
            return self.get(addr-self.start) + (self.get(addr+1-self.start) << 8)
        elif size == 4 and self.isSelected(addr+1) and self.isSelected(addr+2) and self.isSelected(addr+3):
            return self.get(addr-self.start) + (self.get(addr+1-self.start) << 8) + (self.get(addr+2-self.start) << 16) + (self.get(addr+3-self.start) << 24)
       
    def write(self,addr,size,value):
        if not self.isSelected(addr):
            return
        a = value & 0xFF
        b = (value & 0xFF00) >> 8
        c = (value&0xFF0000) >> 16
        d = (value & 0xFF000000) >> 24
            
        if size == 1:
            self.set(addr-self.start,a)
        elif size == 2 and self.isSelected(addr+1):
            self.set(addr-self.start,a)
            self.set(addr+1-self.start,b)
        elif size == 4 and self.isSelected(addr+1) and self.isSelected(addr+2) and self.isSelected(addr+3):
            self.set(addr-self.start,a)
            self.set(addr+1-self.start,b)
            self.set(addr+2-self.start,c)
            self.set(addr+3-self.start,d)
        
    
    def isSelected(self,addr):
        if addr < self.start + self.length and addr >= self.start:
            return True
        return False
        
    def get(self,addr):
        if addr == 0:
            return self.LBA & 0xFF
        if addr == 1:
            return (self.LBA & 0xFF00) >> 8
        if addr == 2:
            return (self.LBA & 0xFF0000) >> 16
        if addr == 3:
            return (self.LBA & 0xFF000000) >> 24
        
        if addr == 4:
            self.block = self.memory[self.LBA*512:(self.LBA*512)+512]
            return 0
        if addr == 5:
            return self.status
        if addr == 6:
            return self.command
        if addr == 7:
            return 0
            
        if addr >= 8 and addr < 520:
            return self.block[addr-8]
            
    def set(self,addr,value):
        if addr == 0:
            self.LBA = (self.LBA & 0xFFFFFF00) | (value & 0xFF)
        if addr == 1:
            self.LBA = (self.LBA & 0xFFFF00FF) | ((value<<8) & 0xFF00)
        if addr == 2:
            self.LBA = (self.LBA & 0xFF00FFFF) | ((value<<16) & 0xFF0000)
        if addr == 3:
            self.LBA = (self.LBA & 0x00FFFFFF) | ((value<<24) & 0xFF000000)
        
        if addr == 4:
            self.memory[self.LBA*512: (self.LBA*512)+512] = self.block
        if addr == 5:
            self.status = value & 0xFF
        if addr == 6:
            self.command = value & 0xFF
        if addr == 7:
            return 0
            
        if addr >= 8 and addr < 520:
            self.block[addr-8] = value & 0xFF
