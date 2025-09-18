import importlib
import json

devices = {}

def loadDevices():
    
    print("Loading devices.")
    devs = json.load(open("devices.json"))
    
    for x in devs.keys():
        try:
            dev = importlib.import_module(devs[x]["deviceType"])
            devices[x] = dev.__getattribute__(devs[x]["device"])(devs[x]["config"])
        except Exception as e:
            print("Failed to load device:",x,e)
    
    print("Devices Loaded, execution after this line.")
    print("-"*80)
    return devices


devices = loadDevices()

def read(addr,size):
    output = 0
    for x in devices.keys():
        e = devices[x].read(addr,size)
        if e:
            output |= e
    return output
    
def write(addr,value,size):
    for x in devices.keys():
        devices[x].write(addr,size,value)


    
    
def tick():
    interrupt = 0
    for x in devices.keys():
        try:
            interrupt = devices[x].tick()
        except:
            pass      
    return interrupt
            
            
