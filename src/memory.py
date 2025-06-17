# Implementation of the Memory class
class Memory():
    #This is the class that allows emulate the Chip8's memory
    def __init__(self):
        self.SIZE = 4096 # This means the 4kB
        self.MEM = [0]*self.SIZE
        self.FONT = [
            #These numbers are the fonts, well, the hex representation of it
            0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
            0x90, 0x90, 0xF0, 0x10, 0x10, # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
            0xF0, 0x10, 0x20, 0x40, 0x40, # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90, # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
            0xF0, 0x80, 0x80, 0x80, 0xF0, # C
            0xE0, 0x90, 0x90, 0x90, 0xE0, # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
            0xF0, 0x80, 0xF0, 0x80, 0x80  # F
        ]
        self.stack = [] # Just the stack to to call subroutines/functions and return from them
        self.stackIndex = 0 #This allows me to access the stack in a more effective way
        self.VX = [0]*16 #General Porpuse Registers
        self.PC = 0x200 #Program Counter, it starts at 0x200 (512dec) because the ROMs, start being loaded from there, we'll use this one to make jumps
        self.I = 0 #Index Register

    #What methods do I need?

    #Print memory
    def printMem(self):
        #This try to print all the 4096 kb, I dont recommend use it, it's better use printMemV2()
        counter = 0
        counterHex = 0x000
        formatedText = ""
        for i in self.MEM:
            if counter == 10:
                print(formatedText)
                formatedText = ""
                counter = 0
            else:
                formatedText += f" |{counterHex:03X}->{self.MEM[i]:03X} |"
                counterHex += 1
                counter +=1

    def printMemV2(self, start, end):
        #This try to print a section of the 4096 kb memory
        """
        The params are:
        start: It can be any number bewteen 000-FFF (0-4096)
        end: It can be any number bewteen 000-FFF (0-4096)
        """
        counter = 0 
        formatedText = ""
        
        if (start > 0xFFF) or (end > 0xFFF):
            print("Please use numbers between the range")
            return
        if (start < 0x000) or (end < 0x000):
            print("Please use numbers between the range")
            return
        
        while start <= end:
            if counter == 5: # Change this number if you want to try another formart, a choose this because it matches with the fonts rows
                print(formatedText)
                formatedText = ""
                counter = 0
            formatedText += f" |{start:03X}->{self.MEM[start]:03X} |"
            counter +=1
            start += 1
    #Print ROMs Instruccions
    
    #Load FONTS
    def loadFont(self):
        start = 0x050
        for i in self.FONT:
            self.MEM[start] = i
            start += 1
    #Load ROM

mem = Memory()
mem.printMemV2(80, 165)
mem.loadFont()
print("_____________________________________")
mem.printMemV2(80, 165)
print("_____________________________________")
mem.printMemV2(0xF00, 0xFFF)
