from ppci.arch.token import Token, bit_range

class JwgOpCodeToken(Token):
    class Info:
        size = 8

    opcode = bit_range(0, 8)
    

class Jwg3RegisterToken(Token):
    class Info:
        size = 10
        
    rd = bit_range(0,5)
    r1 = bit_range(5,10)
    
class Jwg3RegisterToken(Token):
    class Info:
        size = 15
        
    rd = bit_range(0,5)
    r1 = bit_range(5,10)
    r2 = bit_range(10,15)
    
    
    