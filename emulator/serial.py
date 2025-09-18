from queue import Queue
import threading
#import tty
import sys



class telnet:
    def __init__(self,config):
        print("Telnet Serial Device",config)
        from telnetserver import TelnetServer
        from queue import Queue
        import threading
        self.start = config["start"]
        self.port = config["port"]
        self.output_queue = Queue(255)
        self.input_queue = Queue(255)
        self.intterupt = 0


        def update_server(port,out_queue,in_queue):
            server = TelnetServer(port=port)
            clients = []
            while True:
                server.update()
                out = ""
                if not out_queue.empty():
                    while not out_queue.empty():
                        out += chr(out_queue.get())
                    for x in clients:
                        server.send_message(x,out)
                         
                for sender_client, message in server.get_messages():
                    for x in message:
                        in_queue.put(ord(x))
                for new_client in server.get_new_clients():
                    # Add them to the client list 
                    clients.append(new_client)
                for disconnected_client in server.get_disconnected_clients():
                    if disconnected_client not in clients:
                        continue

                    # Remove him from the clients list
                    clients.remove(disconnected_client)
        
        input_thread = threading.Thread(target=update_server, args=([self.port,self.output_queue,self.input_queue]))
        input_thread.daemon = True
        input_thread.start()


        
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
        if addr < self.start + 3 and addr >= self.start:
            return True
        return False
        
    def get(self,addr):
        if addr == 0:
            if self.input_queue.empty():
                return 0
            else:
                return self.input_queue.get()
        if addr == 1:
            return self.input_queue.qsize()
        if addr == 2:
            return self.output_queue.qsize()
        if addr == 3:
            return self.intterupt
            
    def set(self,addr,value):
        if addr == 0:
            self.output_queue.put(value)
        if addr == 3:
            self.intterupt = value



class console:
    def __init__(self,config):
        print("Console Serial Device",config)
        self.start = config["start"]
        self.input_queue = Queue(255)
        #tty.setraw(sys.stdin)
        self.intterupt = 0


        def update_server(in_queue):
            while True:
                t = sys.stdin.read(1)
                if len(t) > 0:
                    in_queue.put(ord(sys.stdin.read(1)))
        
        input_thread = threading.Thread(target=update_server, args=([self.input_queue]))
        input_thread.daemon = True
        input_thread.start()


        
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
        if addr < self.start + 3 and addr >= self.start:
            return True
        return False
        
    def get(self,addr):
        if addr == 0:
            if self.input_queue.empty():
                return 0
            else:
                return self.input_queue.get()
        if addr == 1:
            return self.input_queue.qsize()
        if addr == 2:
            return 0
        if addr == 3:
            return self.intterupt
            
    def set(self,addr,value):
        #print(addr,value)
        if addr == 0:
            sys.stdout.write(chr(value & 0xFF))
            sys.stdout.flush()
        if addr == 3:
            self.intterupt = value