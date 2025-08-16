# This it's going to be the main file of the CHIP-8 emulator.

"""

  /$$$$$$  /$$   /$$ /$$$$$$ /$$$$$$$   /$$$$$$        /$$$$$$$$ /$$      /$$ /$$   /$$ /$$        /$$$$$$  /$$$$$$$$ /$$$$$$  /$$$$$$$ 
 /$$__  $$| $$  | $$|_  $$_/| $$__  $$ /$$__  $$      | $$_____/| $$$    /$$$| $$  | $$| $$       /$$__  $$|__  $$__//$$__  $$| $$__  $$
| $$  \__/| $$  | $$  | $$  | $$  \ $$| $$  \ $$      | $$      | $$$$  /$$$$| $$  | $$| $$      | $$  \ $$   | $$  | $$  \ $$| $$  \ $$
| $$      | $$$$$$$$  | $$  | $$$$$$$/|  $$$$$$/      | $$$$$   | $$ $$/$$ $$| $$  | $$| $$      | $$$$$$$$   | $$  | $$  | $$| $$$$$$$/
| $$      | $$__  $$  | $$  | $$____/  >$$__  $$      | $$__/   | $$  $$$| $$| $$  | $$| $$      | $$__  $$   | $$  | $$  | $$| $$__  $$
| $$    $$| $$  | $$  | $$  | $$      | $$  \ $$      | $$      | $$\  $ | $$| $$  | $$| $$      | $$  | $$   | $$  | $$  | $$| $$  \ $$
|  $$$$$$/| $$  | $$ /$$$$$$| $$      |  $$$$$$/      | $$$$$$$$| $$ \/  | $$|  $$$$$$/| $$$$$$$$| $$  | $$   | $$  |  $$$$$$/| $$  | $$
 \______/ |__/  |__/|______/|__/       \______/       |________/|__/     |__/ \______/ |________/|__/  |__/   |__/   \______/ |__/  |__/

"""
import time
import pygame #for the display
import re # for regular expressions
from display import Display
from memory import Memory

class Chip8():
    def __init__(self):
        self.MEMORY = Memory()
        self.DISPLAY = Display()
    
    def cycle(self):
        #This function it's gonna use the memory and the PC, and it takes a look for the ROM's intructions
        #this function should calls decode_and_execute, and this should use the PC

        PC = self.MEMORY.PC
        firstSet = self.MEMORY.MEM[PC] << 8
        secondSet = self.MEMORY.MEM[PC+1]
        opcode = firstSet | secondSet
        if PC >= 0x200 + self.MEMORY.ROM_SIZE:
            print("End of ROM reached.")
            self.MEMORY.PC = 0x200
            time.sleep(2)
            return
        
        
        self.decode_and_execute(opcode)
        #AND ALSO WE NEED TO INCREMENT THE PC, BUT I THINK THAT WE SHOULD HAVE CARE WITH THIS A THE MOMENT
        self.MEMORY.PC += 2 #This is because the opcodes uses 2 bytes

    def cycle(self):
        #This function it's gonna use the memory and the PC, and it takes a look for the ROM's intructions
        #this function should calls decode_and_execute, and this should use the PC
        increment_pc = True  # por defecto, sumaremos 2 al final

        PC = self.MEMORY.PC
        firstSet = self.MEMORY.MEM[PC] << 8
        secondSet = self.MEMORY.MEM[PC+1]
        opcode = firstSet | secondSet

        if PC >= 0x200 + self.MEMORY.ROM_SIZE:
            print("End of ROM reached.")
            self.MEMORY.PC = 0x200
            time.sleep(2)
            return
        #HERE WE CALL THE DECODE AND EXECUTE FUNCTION
        increment_pc = self.decode_and_execute(opcode)

        if increment_pc:
            self.MEMORY.PC += 2

    def decode_and_execute(self, opcode):
        #this receive the opcodes, and translate them, and execute them
        increment_pc = True

        hexCode = f"{opcode:04X}"
        if hexCode == "00E0":
            #this clean the screen
            self.DISPLAY.clearScreen()
        
        elif hexCode == "00EE":
            #00EE - return from subroutine to address pulled from stack
            self.MEMORY.PC = self.MEMORY.stack.pop()
            increment_pc = False  # ya manejamos el PC
            
        
        elif re.match(r"^1",hexCode):
            # 1NNN - Jump to address NNN → this means we need to set PC = NNN
            NNN = (opcode & 0x0FFF)
            self.MEMORY.PC = NNN
            increment_pc = False  
        
        elif re.match(r"^2", hexCode):
            # 2NNN - push return address onto stack and call subroutine at address NNN
            NNN = opcode & 0x0FFF
            self.MEMORY.stack.append(self.MEMORY.PC + 2)
            # Jump to subrutine
            self.MEMORY.PC = NNN
            increment_pc = False 

        
        elif re.match(r"^3", hexCode):
            #3xnn - skip next opcode if vX == NN
            x = (opcode & 0x0F00) >> 8
            NN = (opcode & 0x00FF)
            if self.MEMORY.VX[x] == NN:
                self.MEMORY.PC += 2 

        elif re.match(r"^4", hexCode):
            #4xnn - skip next opcode if vX != NN
            x = (opcode & 0x0F00) >> 8
            NN = (opcode & 0x00FF)
            if self.MEMORY.VX[x] != NN:
                self.MEMORY.PC += 2 

        elif re.match(r"^5", hexCode):
            #5xy0 - skip next opcode if vX == vY
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            if self.MEMORY.VX[x] == self.MEMORY.VX[y]:
                self.MEMORY.PC += 2 

        
        elif re.match(r"^6",hexCode):
            #6xnn -> set Vx to NN
            # I'm using the r"^6" as my regular expression because there's only one intruction that starts with 6
            x = (opcode & 0x0F00) >> 8 #With this we get the value of X
            nn = (opcode & 0x00FF) #With this we get the value of NN
            self.MEMORY.VX[x] = nn 

        elif re.match(r"^7",hexCode):
            #7xnn -> add NN to vX
            x = (opcode & 0x0F00) >> 8 #With this we get the value of X
            nn = (opcode & 0x00FF) #With this we get the value of NN
            new_value = (self.MEMORY.VX[x] + nn) & 0xFF #to keep the structure of 8bits and dont overflow
            self.MEMORY.VX[x] = new_value

        if re.match(r"^8[0-9A-F][0-9A-F]0$",hexCode):
            #8xy0 - set vX to the value of vY
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            self.MEMORY.VX[x] = self.MEMORY.VX[y]

        if re.match(r"^8[0-9A-F][0-9A-F]1$",hexCode):
            #8xy1 - set vX to the result of bitwise vX OR vY
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            res = self.MEMORY.VX[x] | self.MEMORY.VX[y]
            self.MEMORY.VX[x] = res
            
        if re.match(r"^8[0-9A-F][0-9A-F]2$",hexCode):
            #8xy2 - set vX to the result of bitwise vX AND vY
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            res = self.MEMORY.VX[x] & self.MEMORY.VX[y]
            self.MEMORY.VX[x] = res
            
        if re.match(r"^8[0-9A-F][0-9A-F]3$",hexCode):
            #8xy3 - set vX to the result of bitwise vX XOR vY
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            res = self.MEMORY.VX[x] ^ self.MEMORY.VX[y]
            self.MEMORY.VX[x] = res
            
        if re.match(r"^8[0-9A-F][0-9A-F]4$",hexCode):
            #8xy4 - add vY to vX, vF is set to 1 if an overflow happened, to 0 if not, even if X=F!
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            sum_value = self.MEMORY.VX[x] + self.MEMORY.VX[y]
            self.MEMORY.VX[15] = 1 if sum_value > 255 else 0  # set VF for overflow
            self.MEMORY.VX[x] = sum_value & 0xFF             # keep VX 8-bit

        if re.match(r"^8[0-9A-F][0-9A-F]5$",hexCode):
            #8xy5 - subtract vY from vX, vF is set to 0 if an underflow happened, to 1 if not, even if X=F!
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            self.MEMORY.VX[15] = 1 if self.MEMORY.VX[x] >= self.MEMORY.VX[y] else 0
            self.MEMORY.VX[x] = (self.MEMORY.VX[x] - self.MEMORY.VX[y]) & 0xFF

            
        if re.match(r"^8[0-9A-F][0-9A-F]6$",hexCode):
            #8xy6 - set vX to vY and shift vX one bit to the right, set vF to the bit shifted out, even if X=F!
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            self.MEMORY.VX[15] = self.MEMORY.VX[y] & 0x1
            self.MEMORY.VX[x] = self.MEMORY.VX[y] >> 1
        
        if re.match(r"^8[0-9A-F][0-9A-F]7$",hexCode):
            #8xy7 - set vX to the result of subtracting vX from vY, vF is set to 0 if an underflow happened, to 1 if not, even if X=F!
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            self.MEMORY.VX[15] = 0 if self.MEMORY.VX[y] > self.MEMORY.VX[x] else 1
            self.MEMORY.VX[x] = (self.MEMORY.VX[y] - self.MEMORY.VX[x]) & 0xFF
        
        if re.match(r"^8[0-9A-F][0-9A-F]E$",hexCode):
            #8xyE - set vX to vY and shift vX one bit to the left, set vF to the bit shifted out, even if X=F
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            self.MEMORY.VX[15] = self.MEMORY.VX[y] >> 7
            self.MEMORY.VX[x] = self.MEMORY.VX[y] << 1 & 0xFF
            

        elif re.match(r"^9", hexCode):
            #9xy0 - skip next opcode if vX != vY 
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            if self.MEMORY.VX[x] != self.MEMORY.VX[y]:
                self.MEMORY.PC += 2 




        elif re.match(r"^A",hexCode):
            #Ann -> set I to NNN
            nnn = (opcode & 0x0FFF)
            self.MEMORY.I = nnn


        elif re.match(r"^D",hexCode):
            # Dxyn
            # draw 8xN pixel sprite at position vX, vY with data starting at the address in I, I is not changed
            x = (opcode & 0x0F00) >> 8
            y = (opcode & 0x00F0) >> 4
            I = self.MEMORY.I
            n = (opcode & 0x00F)
            spriteData = self.MEMORY.MEM[I:I+n]
            collision = False

            for row in range(n):
                for col in range(8):
                    if spriteData[row] & (0x80 >> col):
                        collision |= self.DISPLAY.draw_pixel((self.MEMORY.VX[x] + col) % 64, (self.MEMORY.VX[y] + row) % 32)

            if collision:
                self.MEMORY.VX[0xF] = 1
        else:
            print(f"the opcode {hexCode} haven't been implemented yet")

        return increment_pc
    def run(self):
        
        #We need the load the ROM and the FONT
        self.MEMORY.loadFont()
        #self.MEMORY.loadROM("./roms/1-chip8-logo.ch8")
        #self.MEMORY.loadROM("./roms/2-ibm-logo.ch8")
        self.MEMORY.loadROM("./roms/3-corax.ch8")
        
        running = True

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("SALIENDO")
                    running = False

            #SO HERE WE SHOULD HAVE THE CALL TO cycle(), to reflect the changes in the display:
            self.cycle()

            #! self.DISPLAY.draw_pixel(32,16) !THIS WAS JUST TESTING

            # this renders the screen
            self.DISPLAY.render()
            self.DISPLAY.clock.tick(60)  # limits FPS to 60

        pygame.quit()

print("HI!")
chip = Chip8()
chip.run()