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
            #time.sleep(2)
            return
        
        #HERE WE CALL THE DECODE AND EXECUTE FUNCTION
        self.decode_and_execute(opcode)
        #AND ALSO WE NEED TO INCREMENT THE PC, BUT I THINK THAT WE SHOULD HAVE CARE WITH THIS A THE MOMENT
        self.MEMORY.PC += 2 #This is because the opcodes uses 2 bytes

    def decode_and_execute(self, opcode):
        #this receive the opcodes, and translate them, and execute them
        hexCode = f"{opcode:04X}"
        if hexCode == "00E0":
            #this clean the screen
            self.DISPLAY.clearScreen()
        elif re.match(r"^1",hexCode):
            # 1NNN - Jump to address NNN → this means we need to set PC = NNN
            NNN = (opcode & 0x0FFF)
            self.MEMORY.PC = NNN
            pass
        elif re.match(r"^6",hexCode):
            #6xnn -> set Vx to NN
            # I'm using the r"^6" as my regular expression because there's only one intruction that starts with 6
            x = (opcode & 0x0F00) >> 8 #With this we get the value of X
            nn = (opcode & 0x00FF) #With this we get the value of NN
            self.MEMORY.VX[x] = nn # Set Vx to NN in our memory
        elif re.match(r"^7",hexCode):
            #7xnn -> add NN to vX
            x = (opcode & 0x0F00) >> 8 #With this we get the value of X
            nn = (opcode & 0x00FF) #With this we get the value of NN
            self.MEMORY.VX[x] += nn
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
            #time.sleep(2)
            

            if collision:
                self.MEMORY.VX[0xF] = 1
        else:
            print(f"the opcode {hexCode} haven't been implemented yet")

    def run(self):
        
        #We need the load the ROM and the FONT
        self.MEMORY.loadFont()
        #self.MEMORY.loadROM("./roms/1-chip8-logo.ch8")
        self.MEMORY.loadROM("./roms/2-ibm-logo.ch8")
        
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