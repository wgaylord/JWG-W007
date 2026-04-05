import cpu
import mmu
import time
import sys



cpu = cpu.CPU(readFunc = mmu.read, writeFunc = mmu.write)

while True:
    if (cpu.PC >= 10240):
        print(hex(cpu.PC))
    cpu.tick()
    interrupt = mmu.tick()
    if interrupt > 0:
        cpu.interrupt(interrupt)
    time.sleep(0.0001)
    
print("Go")