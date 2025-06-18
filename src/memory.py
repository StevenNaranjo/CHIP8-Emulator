# Implementation of the Memory class
import time


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
        self.ROM_SIZE = 0 # I'll use this to print all the ROM content 

    #What methods do I need?

    #Load FONTS
    def loadFont(self):
        start = 0x050
        for i in self.FONT:
            self.MEM[start] = i
            start += 1

    #Load ROM
    def loadROM(self, ROM):
        # Load a .ch8 (the file extension for the roms of chip8) file in the memory
        try:
            with open(ROM, 'rb') as file: # rb stands for read binary
                rom_data = file.read()
                self.ROM_SIZE = len(rom_data)
                for i in range(len(rom_data)):
                    self.MEM[0x200 + i] = rom_data[i]
                print("ROM loaded succesfully")
        except FileNotFoundError:
            print(f"Error: ROM file '{ROM}' not found.")
        except Exception as e:
            print(f"An error occurred while loading the ROM: {e}")

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
                formatedText += f" |{counterHex:03X}->{self.MEM[i]:02X} |"
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
            formatedText += f" |{start:03X}->{self.MEM[start]:02X} |"
            counter +=1
            start += 1

    def printInstructions(self):
        # This function print the set of instruccions in a pretty way to easy understanding
        """
            How does this work?
            Suppose that we have the following bytes in memory:
                
            self.MEM[0x200]     = 0xA2   binary 10100010
            self.MEM[0x201]     = 0xF0   binary 11110000
            
            So we want to combine these two bytes into one 16-bit instruction (2bytes).
            First, we shift the first byte (0xA2) 8 bits to the left:
    
                0xA2 << 8 = 0xA200 = 10100010 00000000

            Then, we use the OR operator '|' to combine it with the second byte (0xF0):
                10100010 00000000   (0xA2 shifted left)
            OR  00000000 11110000   (0xF0)
                --------------------
                10100010 11110000   => 0xA2F0

            So the full instruction is now correctly combined into 0xA2F0.
        """
        instructions = ""
        counter = 0
        start = 0x200
        i = 0

        while i < self.ROM_SIZE - 1:
            if counter == 8:
                print(instructions)
                instructions = ""
                counter = 0
            instr = (self.MEM[start + i] << 8) | self.MEM[start + i + 1] #this is a bit shift so of this way we can combine the set of instruction
            instructions += f" |{instr:04X}|" # f" |{start+i:03X}-{start+i+1:03X}:{instr:04X} |" use this if you wanna see the mem direction
            i += 2
            counter += 1

        # if ROM_SIZE is odd
        if i < self.ROM_SIZE:
            last_byte = self.MEM[start + i]
            instructions += f" |{start+i:03X}: {last_byte:02X} (dangling byte) |"

        if instructions:  # Print wha
            print(instructions)

mem = Memory()
print("__________________Memory before load the FONTS___________________")
mem.printMemV2(80, 165)
mem.loadFont()
print("__________________Memory after load the FONTS___________________")
mem.printMemV2(80, 165)
print("__________________ROM-Loaded___________________")
mem.loadROM("./roms/1-chip8-logo.ch8") #Change this based in your SO, in my case Im from linux
print("__________________ROM___________________")
end = mem.ROM_SIZE + 0x200
mem.printMemV2(0x200, end)
print("__________________Instructions___________________")
mem.printInstructions()