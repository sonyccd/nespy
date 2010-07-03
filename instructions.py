import hardware

#getting registers (the list indexes)
I_F = 5
N_F = 0
Z_F = 6


#Sign flag: this is set if the result of an operation is
#negative, cleared if positive.
def setN(nesSystem, result):
    if ord(result) < 0:
        nesSystem.cpu.status[N_F] = 1
    else:
        nesSystem.cpu.status[N_F] = 0

#Zero flag: this is set to 1 when any arithmetic or logical
#operation produces a zero result, and is set to 0 if the result is
#non-zero.        
def setZ(nesSystem, result):
    if ord(result) == 0:
        nesSystem.cpu.status[Z_F] = 1
    else:
        nesSystem.cpu.status[Z_F] = 0


def pushStack(nesSystem, byte):
    nesSystem.cpu.cpuMemory[nesSystem.cpu.stackP - 1 + 0x100] = byte
    
def popStack(nesSystem):
    return nesSystem.cpu.cpuMemory[nesSystem.cpu.stackP + 1 + 0x101]        
        
#0x78. Set interrupt disable status
def SEI(nesSystem, cpu):
    nesSystem.cpu.status[I_F] = 1
   
#0xD8. Clear decimal mode
def CLD(nesSystem, cpu):
    pass
    
#0xA9. Load accumulator with memory IMMEDIATE
def LDA_Immediate(nesSystem, cpu):
    cpu.operand = cpu.getNextByte()
    nesSystem.cpu.accumulator = cpu.operand
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    
#0x10. Branch on result plus. Jump back the RELATIVE number of bytes. 
#If the operand was FB, then we jump back FB - FF+1 number of bytes (-5) 
def BPL(nesSystem, cpu):
    cpu.operand = cpu.getNextByte()
    if nesSystem.cpu.status[N_F] == 0:
        nesSystem.cpu.programCounter += (ord(cpu.operand) - (0xFF + 1)) 
        
#0x8D. Store the byte in the accumulator into memory     
def STA_Absolute(nesSystem, cpu):
    cpu.operand = cpu.getNextWord()
    nesSystem.cpu.cpuMemory[ord(cpu.operand)] = nesSystem.cpu.accumulator
       
def JSR(nesSystem, cpu):
    pass
 
#0xA2. load register X with next byte
def LDX(nesSystem, cpu):
    cpu.operand = cpu.getNextByte()
    nesSystem.cpu.registerX =  cpu.operand
    setN(nesSystem, nesSystem.cpu.registerX)
    setZ(nesSystem, nesSystem.cpu.registerX)
    
#0x9A. Transfers the byte in X Register into the Stack Pointer. Not many roms use this
def TXS(nesSystem, cpu):
    #nesSystem.cpu.stackP = nesSystem.cpu.registerX
    pushStack(nesSystem, nesSystem.cpu.registerX)
    
    
    
#0xAD. Transfers the byte in X Register into the Stack Pointer. Not many roms use this
def LDA_Absolute(nesSystem, cpu):
    cpu.operand = cpu.getNextWord()
    nesSystem.cpu.accumulator = nesSystem.cpu.cpuMemory[ord(cpu.operand)]
    setN(nesSystem, nesSystem.cpu.accumulator)
    setZ(nesSystem, nesSystem.cpu.accumulator)
    
    
    #nesSystem.cpu.stackP = nesSystem.cpu.registerX
    