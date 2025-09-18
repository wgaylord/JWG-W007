import cpu
import board
import mmu
import time



cpu = cpu.CPU(readFunc = board.read, writeFunc = board.write)

while True:
    #print(cpu.PC,cpu.registers)
    cpu.tick()
    time.sleep(0.1)
    