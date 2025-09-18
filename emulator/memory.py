class RAM:
    def __init__(self,config):
        print("RAM Device",config)
        self.start = config["start"]
        self.length = config["length"]
        self.memory = {}

        
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
        if addr in self.memory.keys():
            return self.memory[addr]
        else:
            return 0
            
    def set(self,addr,value):
        self.memory[addr] = value  
        if value == 0:
            del self.memory[addr]
        
class ROM:
    def __init__(self,config):
        print("ROM Device",config)
        self.start = config["start"]
        self.length = config["length"]
        self.data = open(config["binary"],"rb").read()
    
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
        return
        
    
    def isSelected(self,addr):
        if addr < self.start + self.length and addr >= self.start:
            return True
        return False
        
    def get(self,addr):
        if addr < len(self.data):
            return self.data[addr]
        else:
            return 0
            