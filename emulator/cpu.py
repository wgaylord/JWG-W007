from functools import partial


INT_RA = 31
STATUS = 30
RETURN_ADDR = 29

PRIVLAGED_CSR_OFFSET = 2147483648


class STATUS_BITS:
    OverFlow8 = 1
    OverFlow16 = 2
    OverFlow32 = 4
    ZERO = 8
    EQUAL = 16
    GREATER = 32
    MACHINE_MODE = 64
 

 


class CPU:
    
    __MultiWordInstructions = [0x2,0x3,0x4,0x5,0x6,0x9,0x16,0x18,0x1D]
    __Const = [0,1]
    
    def __init__(self,readFunc,writeFunc):
        self.readByte = partial(readFunc,size=1)
        self.readHalf = partial(readFunc,size=2)
        self.readWord = partial(readFunc,size=4)
        
        self.writeByte = partial(writeFunc,size=1)
        self.writeHalf = partial(writeFunc,size=2)
        self.writeWord = partial(writeFunc,size=4)
        
        
        self.PC = 0
        
        self.registers = {}
        
        for x in range(32):
            self.registers[x] = 0
            
        self.registers[1] = 1
    
    def interrupt(self,number):
        self.registers[INT_RA] = self.PC
        self.PC = self.readWord(-(((number&0xFF)*4)+PRIVLAGED_CSR_OFFSET))
        return
        
    def tick(self):
        instruction = self.readWord(self.PC)
        
        opcode = instruction>>27
        rd = (instruction>>22) & 0b11111
        r1 = (instruction>>17) & 0b11111
        r2 = (instruction>>12) & 0b11111
        cond = (instruction>>8) & 0b11111111
        immd = 0
        
        if opcode in self.__MultiWordInstructions:
            immd = self.readWord(self.PC+4)
        #print(opcode)
        match opcode:
            case 0:
                self.PC = self.PC + 4
                return
                
            case 1:
                addr = immd + self.registers[r1]
                self.registers[rd] = self.readWord(addr)
                self.PC = self.PC + 8
                return
            case 2:
                addr = immd + self.registers[r1]
                self.registers[rd] = self.readHalf(addr)
                self.PC = self.PC + 8
                return
            case 3:
                addr = immd + self.registers[r1]
                self.registers[rd] = self.readByte(addr)
                self.PC = self.PC + 8
                return
                
            case 4:
                addr = immd + self.registers[r1]
                self.writeWord(addr,self.registers[r2])
                self.PC = self.PC + 8
                return
            case 5:
                addr = immd + self.registers[r1]
                self.writeHalf(addr,self.registers[r2])
                self.PC = self.PC + 8
                return   
            case 6:
                addr = immd + self.registers[r1]
                self.writeByte(addr,self.registers[r2])
                self.PC = self.PC + 8
                return                   
                
            case 7:
                self.PC = self.PC + 4
                return
            
            case 8:
                self.PC = self.PC + 4
                return
                
            case 9:
                self.registers[rd] = immd
                self.PC = self.PC + 8
                return
                
            case 10:
                temp = self.registers[r1] + self.registers[r2]
                
                if temp > 0xFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow8
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow8 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow16
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow16 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFFFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow32
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow32 ^ 0xFFFFFFFF) & self.registers[STATUS]
                
                if temp == 0:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.ZERO
                else:
                    self.registers[STATUS] = (STATUS_BITS.ZERO ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                    
                self.registers[rd] = temp & 0xFFFFFFFF
                
                self.PC = self.PC + 4
                return
            
            case 11:
                temp = self.registers[r1] - self.registers[r2]
                
                if temp > 0xFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow8
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow8 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow16
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow16 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFFFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow32
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow32 ^ 0xFFFFFFFF) & self.registers[STATUS]
                
                if temp == 0:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.ZERO
                else:
                    self.registers[STATUS] = (STATUS_BITS.ZERO ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                    
                self.registers[rd] = temp & 0xFFFFFFFF
                
                self.PC = self.PC + 4
                return
                
            case 12:
                temp = self.registers[r1] * self.registers[r2]
                
                if temp > 0xFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow8
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow8 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow16
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow16 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFFFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow32
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow32 ^ 0xFFFFFFFF) & self.registers[STATUS]
                
                if temp == 0:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.ZERO
                else:
                    self.registers[STATUS] = (STATUS_BITS.ZERO ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                    
                self.registers[rd] = temp & 0xFFFFFFFF
                
                self.PC = self.PC + 4
                return
                
            case 13:
                temp = self.registers[r1] // self.registers[r2]
                
                if temp > 0xFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow8
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow8 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow16
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow16 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFFFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow32
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow32 ^ 0xFFFFFFFF) & self.registers[STATUS]
                
                if temp == 0:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.ZERO
                else:
                    self.registers[STATUS] = (STATUS_BITS.ZERO ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                    
                self.registers[rd] = temp & 0xFFFFFFFF
                
                self.PC = self.PC + 4
                return
                
                
            case 14:
                temp = self.registers[r1] << 1
                
                if temp > 0xFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow8
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow8 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow16
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow16 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFFFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow32
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow32 ^ 0xFFFFFFFF) & self.registers[STATUS]
                
                if temp == 0:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.ZERO
                else:
                    self.registers[STATUS] = (STATUS_BITS.ZERO ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                    
                self.registers[rd] = temp & 0xFFFFFFFF
                
                self.PC = self.PC + 4
                return
                
            case 15:
                temp = self.registers[r1] >> 1
                
                if temp > 0xFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow8
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow8 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow16
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow16 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFFFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow32
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow32 ^ 0xFFFFFFFF) & self.registers[STATUS]
                
                if temp == 0:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.ZERO
                else:
                    self.registers[STATUS] = (STATUS_BITS.ZERO ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                    
                self.registers[rd] = temp & 0xFFFFFFFF
                
                self.PC = self.PC + 4
                return
                
            case 16:
                temp = self.registers[r1] & self.registers[r2]
                
                if temp > 0xFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow8
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow8 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow16
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow16 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFFFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow32
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow32 ^ 0xFFFFFFFF) & self.registers[STATUS]
                
                if temp == 0:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.ZERO
                else:
                    self.registers[STATUS] = (STATUS_BITS.ZERO ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                    
                self.registers[rd] = temp & 0xFFFFFFFF
                
                self.PC = self.PC + 4
                return
                
            case 17:
                temp = self.registers[r1] | self.registers[r2]
                
                if temp > 0xFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow8
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow8 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow16
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow16 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFFFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow32
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow32 ^ 0xFFFFFFFF) & self.registers[STATUS]
                
                if temp == 0:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.ZERO
                else:
                    self.registers[STATUS] = (STATUS_BITS.ZERO ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                    
                self.registers[rd] = temp & 0xFFFFFFFF
                
                self.PC = self.PC + 4
                return
                
                
            case 18:
                temp = self.registers[r1] ^ self.registers[r2]
                
                if temp > 0xFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow8
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow8 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow16
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow16 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFFFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow32
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow32 ^ 0xFFFFFFFF) & self.registers[STATUS]
                
                if temp == 0:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.ZERO
                else:
                    self.registers[STATUS] = (STATUS_BITS.ZERO ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                    
                self.registers[rd] = temp & 0xFFFFFFFF
                
                self.PC = self.PC + 4
                return
                
                
            case 19: # NOT
                temp = (~self.registers[r1]) & 0xFFFFFFFF
                
                if temp > 0xFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow8
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow8 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow16
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow16 ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if temp > 0xFFFFFFFF:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.OverFlow32
                else:
                    self.registers[STATUS] = (STATUS_BITS.OverFlow32 ^ 0xFFFFFFFF) & self.registers[STATUS]
                
                if temp == 0:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.ZERO
                else:
                    self.registers[STATUS] = (STATUS_BITS.ZERO ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                    
                self.registers[rd] = temp & 0xFFFFFFFF
                
                self.PC = self.PC + 4
                return
                
            case 20: #cmps
                
                r1s = ((~self.registers[r1]) & 0xFFFFFFFF) + 1 
                r2s = ((~self.registers[r2]) & 0xFFFFFFFF) + 1
                
                if r1s == r2s:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.EQUAL
                else:
                    self.registers[STATUS] = (STATUS_BITS.EQUAL ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if r1s > r2s:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.EQUAL
                else:
                    self.registers[STATUS] = (STATUS_BITS.EQUAL ^ 0xFFFFFFFF) & self.registers[STATUS]
               
                
                self.PC = self.PC + 4
                return
                
            case 21: #cmpu
                r1s =  self.registers[r1] 
                r2s = self.registers[r2]
                #print("cmpu",r1s,r2s,r1s == r2s,r1s > r2s)
                if r1s == r2s:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.EQUAL
                else:
                    self.registers[STATUS] = (STATUS_BITS.EQUAL ^ 0xFFFFFFFF) & self.registers[STATUS]
                    
                if r1s > r2s:
                    self.registers[STATUS] = self.registers[STATUS] | STATUS_BITS.GREATER
                else:
                    self.registers[STATUS] = (STATUS_BITS.GREATER ^ 0xFFFFFFFF) & self.registers[STATUS]
              
                self.PC = self.PC + 4
                return
                
            case 22: #bchi
                
                #print("Branch Instruction",cond,self.registers[STATUS] & cond == cond)
                if self.registers[STATUS] & cond == cond or cond == 0:
                    self.PC = immd
                    return
                
                self.PC = self.PC + 8
                return
                
            case 23: #bchr
                if self.registers[STATUS] & cond == cond or cond == 0:
                    self.PC = self.registers[r1] 
                    return
                
                self.PC = self.PC + 4
                return
                
            case 24: #call
                self.registers[RETURN_ADDR] = self.PC + 8
                self.PC = immd
                #print(self.PC)
                return
                            
            case 25: #callr
                self.registers[RETURN_ADDR] = self.PC + 4
                self.PC = self.registers[r1] 
                return
                
            case 26: #rtn
                self.PC = self.registers[RETURN_ADDR] 
                return
                
                
            case 27: #wctl
                self.PC = self.PC + 4
                if self.registers[r1] >= PRIVLAGED_CSR_OFFSET and self.registers[STATUS] & STATUS_BITS.MACHINE_MODE != STATUS_BITS.MACHINE_MODE:
                    self.registers[INT_RA] = self.PC
                    self.PC = self.readWord(-(PRIVLAGED_CSR_OFFSET))
                    return
                self.writeWord(-self.registers[r1],self.registers[r2])
                return
                
            case 28: #rctl
                self.PC = self.PC + 4
                if self.registers[r1] >= PRIVLAGED_CSR_OFFSET and self.registers[STATUS] & STATUS_BITS.MACHINE_MODE != STATUS_BITS.MACHINE_MODE:
                    self.registers[INT_RA] = self.PC
                    self.PC = self.readWord(-(PRIVLAGED_CSR_OFFSET))
                    return
                self.registers[rd] = self.readWord(-self.registers[r1])
                return
            
            

            case 29: #aswap
                self.PC = self.PC + 8
                self.registers[rd] = self.readWord(addr)
                self.writeWord(addr,self.registers[r1])
                
                return
                
            case 30: #syscall
                self.PC = self.PC + 8
                self.registers[INT_RA] = self.PC
                self.PC = self.readWord(-(((self.registers[r1]&0xFF)*4)+PRIVLAGED_CSR_OFFSET))
                return
                
            case 21: #sysrtn
                self.PC = self.registers[INT_RA]
                return