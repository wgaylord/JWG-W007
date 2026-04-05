import board

privilegeMode = 0

def read(addr,size):
    return board.read(addr,size)
    
def write(addr,value,size):
    board.write(addr,value,size)
    
    
def tick():
    return board.tick()
            
            
