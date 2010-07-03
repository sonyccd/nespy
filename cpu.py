import hardware
import romloader
import instructions

class cpu:

    def __init__(self, nes): 
        self.nesSystem = nes
        self.operand = 0
    
    def getNextByte(self):
        self.nesSystem.cpu.programCounter += 1
        return self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter]
        
    def getNextWord(self):
        self.nesSystem.cpu.programCounter += 1

        self.operand = ord(self.operand) | (ord(self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter]) << 8)
        return self.nesSystem.cpu.cpuMemory[self.nesSystem.cpu.programCounter + 1]
        

    def memoryInit(self):
        for x in range(len(self.nesSystem.rom.prgData)):
            self.nesSystem.cpu.cpuMemory[x + 0x8000] = self.nesSystem.rom.prgData[x]
        
        # if ord(self.nesSystem.rom.controlByte1) & self.nesSystem.rom.SRAM_MASK:
            # print "SRAM"
        
        # if ord(self.nesSystem.rom.controlByte1) & self.nesSystem.rom.TRAINER_MASK:
            # print "SRAM"
        
    def cpuInit(self):

        #PC = byte at 0xFFFD * 256 + byte at 0xFFFC 
        self.nesSystem.cpu.programCounter = (ord(self.nesSystem.cpu.cpuMemory[0xFFFD]) * 256) + ord(self.nesSystem.cpu.cpuMemory[0xFFFC]) - 1
        self.nesSystem.cpu.stackP = 0xFF
        self.nesSystem.cpu.accumulator = 0
        self.nesSystem.cpu.xIndex = 0
        self.nesSystem.cpu.yIndex = 0
        self.nesSystem.cpu.status = 0
        
    
        
    def execute(self):
        
        
        currentOpCode = hex(ord(self.getNextByte()))

        
        #dict containing the 6502's opcodes
        opCodes = {
                    "0x78" : instructions.SEI,
                    "0xd8" : instructions.CLD,
                    "0xa9" : instructions.LDA,
                    "0x10" : instructions.BPL,
                    "0x8d" : instructions.STA_bbbb,
                    
                  }
        #execute the instruction corresponding with the opcode signature          
        opCodes[currentOpCode](self.nesSystem, self)
        print hex(self.nesSystem.cpu.programCounter)