import socket
import cpu
import board
import mmu
import struct


HOST = '0.0.0.0' 
PORT = 2000 

blockSize = 1024
 
# 0 = tick - Takes a single byte parm of ticks to run
# 1 = peek - Takes a byte for size ( 1, 2, 4) and 4 bytes for address returns 4 bytes for value
# 2 = poke - Takes a byte for size ( 1, 2, 4) and 4 bytes for address and 4 bytes for value
# 3 = block_peek - Takes 4 bytes for address returns 1024 bytes of data
# 4 = block_poke - Takes 4 bytes for address and 1024 bytes of data
# 5 = return all cpu registers - Length Prefixed array of 4 bytes numbers
# 6 = set cpu register - Takes 1 byte for register addrs and 4 bytes for data

cpu = cpu.CPU(readFunc = board.read, writeFunc = board.write)

def run_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Debug server listening on {HOST}:{PORT}")
        while True:
            try:
                
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(blockSize + 4 + 1)
                        if not data:
                            break
                            
                        if data[0] == 0:
                            try:
                                times = data[1]
                                for x in range(times):
                                    cpu.tick()
                                    interrupt = board.tick()
                                    if interrupt > 0:
                                        cpu.interrupt(interrupt)
                                conn.sendall(b"TICKED")
                            except Exception as e:
                                conn.sendall(bytes(e))
                            continue
                        if data[0] == 1:
                            try:
                                size = data[1]
                                address = struct.unpack(">I",data[2:6])[0]
                                conn.sendall(struct.pack(">I",board.read(address,size)))
                            except Exception as e:
                                conn.sendall(bytes(str(e),"ascii"))
                            continue
                        if data[0] == 2:
                            try:
                                size = data[1]
                                address = struct.unpack(">I",data[2:6])[0]
                                value = struct.unpack(">I",data[6:10])[0]
                                board.write(address,value,size)
                                conn.sendall(b"SET")
                            except Exception as e:
                                conn.sendall(bytes(e))
                            continue 
                        if data[0] == 3:
                            try:
                                address = struct.unpack(">I",data[1:5])[0]
                                data1 = []
                                for x in range(1024):
                                    data1.append(board.read(address+x,1))
                                conn.sendall(bytes(data1))
                            except Exception as e:
                                conn.sendall(bytes(e))
                            continue 
                        if data[0] == 4:
                            try:
                                address = struct.unpack(">I",data[1:5])[0]
                                value = data[5:]
                                for x in range(1024):
                                    board.write(address+x,value[x],1)
                                conn.sendall(b"SET BLOCK")
                            except Exception as e:
                                conn.sendall(bytes(e))
                            continue 
                        if data[0] == 5:
                            try:
                                data1 = struct.pack(">B",32)
                                for x in range(32):
                                    data1 += struct.pack(">I",cpu.registers[x])
                                #print(data1)
                                conn.sendall(data1)
                            except Exception as e:
                                conn.sendall(bytes(e))
                            continue 
                        if data[0] == 6:
                            try:
                                reg = data[1]
                                value = struct.unpack(">I",data[2:6])[0]
                                cpu.registers[reg] = value
                                conn.sendall(b"Register Set")
                            except Exception as e:
                                conn.sendall(bytes(e))
                            continue 
            except Exception as e:
                print(e)
                    

if __name__ == "__main__":
    run_server()