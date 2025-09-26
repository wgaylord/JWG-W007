import cpu
import board
import mmu
import time



cpu = cpu.CPU(readFunc = board.read, writeFunc = board.write)

while True:
    #print(hex(cpu.PC),cpu.registers)
    cpu.tick()
    interrupt = board.tick()
    if interrupt > 0:
        cpu.interrupt(interrupt)
    time.sleep(0.01)
    