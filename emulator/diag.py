import sys


class diag:
    def __init__(self,config):
        self.watched = config["watched"]
        print(self.watched)


        
    def read(self,addr,size):
        if addr in self.watched:
            print("Read: ",addr," size ",size,"\n")
            sys.stdout.flush()
        
        return 0
       
    def write(self,addr,size,value):
        if addr in self.watched:
            print("Wrote: ",addr," with value ",value, " size ",size,"\n")
            sys.stdout.flush()
        