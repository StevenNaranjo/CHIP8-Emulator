# CHIP8-Emulator
A functional CHIP-8 emulator written in Python.

- Based on the guide of **[Tobias V. Langhoff](https://tobiasvl.github.io/blog/write-a-chip-8-emulator/#font)**
- And following this **[Opcode Table](https://chip8.gulrak.net/)** 
- And also based on this YouTube video: **[Haz tu primer emulador. Chip-8](https://www.youtube.com/watch?v=FT8gkGETgcg)**
- And all the ROMs, were get from **[chip8-test-suite](https://github.com/Timendus/chip8-test-suite)**

> I'm going to use **PyGame** to build the display 
> And **re** for regular expression to decode the opcodes :D

## Based On the Guide of Tobias the Chip8 specifications are:

- Memory: CHIP-8 has direct access to up to 4 kilobytes of RAM
- Display: 64 x 32 pixels (or 128 x 64 for SUPER-CHIP) monochrome, ie. black or white
- A program counter, often called just “PC”, which points at the current instruction in memory
- One 16-bit index register called “I” which is used to point at locations in memory
- A stack for 16-bit addresses, which is used to call subroutines/functions and return from them
- An 8-bit delay timer which is decremented at a rate of 60 Hz (60 times per second) until it reaches 0
- An 8-bit sound timer which functions like the delay timer, but which also gives off a beeping sound as long as it’s not 0
- 16 8-bit (one byte) general-purpose variable registers numbered 0 through F hexadecimal, ie. 0 through 15 in decimal, called V0 through VF
    - VF is also used as a flag register; many instructions will set it to either 1 or 0 based on some rule, for example using it as a carry flag

### Opcodes
|Opcode | Description                                                                                                                       | Implemented?  |
|-------|-----------------------------------------------------------------------------------------------------------------------------------|---------------|
|00E0   |clear the screen                                                                                                                   |Yes             |
|00EE   |return from subroutine to address pulled from stack                                                                                |No             |
|0nnn   |jump to native assembler subroutine at 0xNNN                                                                                       |No             |
|1nnn   |jump to address NNN                                                                                                                |Yes             |
|2nnn   |push return address onto stack and call subroutine at address NNN                                                                  |No             |
|3xnn   |skip next opcode if vX == NN                                                                                                       |No             |
|4xnn   |skip next opcode if vX != NN                                                                                                       |No             |
|5xy0   |skip next opcode if vX == vY                                                                                                       |No             |
|6xnn   |set vX to NN                                                                                                                       |Yes             |
|7xnn   |add NN to vX                                                                                                                       |Yes             |
|8xy0   |set vX to the value of vY                                                                                                          |No             |
|8xy1   |set vX to the result of bitwise vX OR vY                                                                                           |No             |
|8xy2   |set vX to the result of bitwise vX AND vY                                                                                          |No             |
|8xy3   |set vX to the result of bitwise vX XOR vY                                                                                          |No             |
|8xy4   |add vY to vX, vF is set to 1 if an overflow happened, to 0 if not, even if X=F!                                                    |No             |
|8xy5   |subtract vY from vX, vF is set to 0 if an underflow happened, to 1 if not, even if X=F!                                            |No             |
|8xy6   |set vX to vY and shift vX one bit to the right, set vF to the bit shifted out, even if X=F!                                        |No             |
|8xy7   |set vX to the result of subtracting vX from vY, vF is set to 0 if an underflow happened, to 1 if not, even if X=F!                 |No             |
|8xyE   |set vX to vY and shift vX one bit to the left, set vF to the bit shifted out, even if X=F!                                         |No             |
|9xy0   |skip next opcode if vX != vY (note: on platforms that have 4 byte opcodes, like F000 on XO-CHIP, this needs to skip four bytes)    |No             |
|Annn   |set I to NNN                                                                                                                       |Yes             |
|Bnnn   |jump to address NNN + v0                                                                                                           |No             |
|Cxnn   |set vx to a random value masked (bitwise AND) with NN                                                                              |No             |
|Dxyn   |draw 8xN pixel sprite at position vX, vY with data starting at the address in I, I is not changed                                  |Yes             |
|Ex9E   |skip next opcode if key in the lower 4 bits of vX is pressed                                                                       |No             |
|ExA1   |skip next opcode if key in the lower 4 bits of vX is not pressed                                                                   |No             |
|Fx07   |set vX to the value of the delay timer                                                                                             |No             |
|Fx0A   |wait for a key pressed and released and set vX to it, in megachip mode it also updates the screen like clear                       |No             |
|Fx15   |set delay timer to vX                                                                                                              |No             |
|Fx18   |set sound timer to vX, sound is played as long as the sound timer reaches zero                                                     |No             |
|Fx1E   |add vX to I                                                                                                                        |No             |
|Fx29   |set I to the 5 line high hex sprite for the lowest nibble in vX                                                                    |No             |
|Fx33   |write the value of vX as BCD value at the addresses I, I+1 and I+2                                                                 |No             |
|Fx55   |write the content of v0 to vX at the memory pointed to by I, I is incremented by X+1                                               |No             |
|Fx65   | read the bytes from memory pointed to by I into the registers v0 to vX, I is incremented by X+1                                   |No             |


### The Memory:
This memory has a size or 4kB (4096 bytes)
The Program Counter (known as **PC**), Index Register (often called **"I"**), and the stack; are all 16 bits long

Based on the guide of Tobias, the first interpeter was also located in RAM, from adress 000 to 1FF (0->511). So the PC (Program Counter starts at 200hex (512dec))

> I'm not a master at numeric bases convertor, so Im going to use a converter all the time to get decimal from a hex.

The font should be in the memory. So we have that after the 512 byte it'll be loaded the ROM, so we can used any value between 0 and 511, but according Tobias, for some reason the place most popular to load the font, it's 050-09F (80-159)

The most common used font it's: 

| Hex | Bytes                          |
|-----|--------------------------------|
| 0   | 0xF0, 0x90, 0x90, 0x90, 0xF0   |
| 1   | 0x20, 0x60, 0x20, 0x20, 0x70   |
| 2   | 0xF0, 0x10, 0xF0, 0x80, 0xF0   |
| 3   | 0xF0, 0x10, 0xF0, 0x10, 0xF0   |
| 4   | 0x90, 0x90, 0xF0, 0x10, 0x10   |
| 5   | 0xF0, 0x80, 0xF0, 0x10, 0xF0   |
| 6   | 0xF0, 0x80, 0xF0, 0x90, 0xF0   |
| 7   | 0xF0, 0x10, 0x20, 0x40, 0x40   |
| 8   | 0xF0, 0x90, 0xF0, 0x90, 0xF0   |
| 9   | 0xF0, 0x90, 0xF0, 0x10, 0xF0   |
| A   | 0xF0, 0x90, 0xF0, 0x90, 0x90   |
| B   | 0xE0, 0x90, 0xE0, 0x90, 0xE0   |
| C   | 0xF0, 0x80, 0x80, 0x80, 0xF0   |
| D   | 0xE0, 0x90, 0x90, 0x90, 0xE0   |
| E   | 0xF0, 0x80, 0xF0, 0x80, 0xF0   |
| F   | 0xF0, 0x80, 0xF0, 0x80, 0x80   |

The implementation of this, it's on `src/memory.py` 

### The Display

According to Tobias the display's size is 64 pixels wide and 32 pixels tall. And each pixel can be on or off. 
But this is so small so, I am going to use a scale about to 10, to get a moderate size
The display has a refresh rate of 60hz (60FPS)

> Based on **[Tobias](https://tobiasvl.github.io/blog/write-a-chip-8-emulator/#display)**: The details of the drawing instruction DXYN are found below, but in short, it is used to draw a “sprite” on the screen. Each sprite consists of 8-bit bytes, where each bit corresponds to a horizontal pixel; sprites are between 1 and 15 bytes tall. They’re drawn to the screen by treating all 0 bits as transparent, and all the 1 bits will “flip” the pixels in the locations of the screen that it’s drawn to. (You might recognize this as logical XOR.)

The implementation of this, it's on `src/display.py`
> By the way, I've never worked with PyGame before, so I need to take a look to the **[Documentation](https://www.pygame.org/docs/)** 

### The Chip8 

This is the main class, this one, have all the previous classes. 

#### It's on charge of the following things:

- **Fetch** the instruction from memory at the current PC (program counter)
- **Decode** the instruction to find out what the emulator should do
- **Execute** the instruction and do what it tells you


The implementation of this, it's on `src/chip8.py`

## ROMs

### Splash Screen:
The first test is a very simple splash screen. 

To make this ROM run we'll need to implement the following opcodes:
> - `00E0` - Clear the screen 
> - `6xnn` - Load normal register with immediate value
> - `Annn` - Load index register with immediate value
> - `Dxyn` - Draw sprite to screen (only aligned)

### IBM logo
This one draws the IBM logo on the display

To make this ROM run we'll need to implement the following opcodes:
> - 00E0 - Clear the screen
> - 6xnn - Load normal register with immediate value
> - Annn - Load index register with immediate value
> - 7xnn - Add immediate value to normal register
> - Dxyn - Draw sprite to screen (un-aligned)


## 🤓 Terms

### G 
- **General Purpose Registers**: Registers inside a CPU used to temporarily hold data, addresses, or results of operations. They can be used for a wide range of tasks during instruction execution.

---

### I
- **Index Register**: A special register that holds a memory address used to indirectly access data in RAM, often in loops or array-like structures.

---

### J 
- **Jump**: An instruction that changes the normal sequential flow of a program by moving the instruction pointer (or program counter) to a new memory address.

---

### P
- **Program Counter**: A register that holds the address of the next instruction to execute. It updates automatically as the program runs, and can be modified directly by jumps, calls, or branches.

---

### R  
- **Register**: A small, fast storage location within the CPU used to store data, addresses, or instructions during computation. Registers are faster than RAM and essential to processor operations.
- **ROM**: Stands for Read-Only Memory
---

### S   
- **Stack**: A data structure that follows the Last In, First Out (LIFO) principle. It is used to store return addresses, function calls, or local variables, and is manipulated with push and pop operations.

---

**Built with ❤️ by Alex Naranjo**  
**Costa Rica 🇨🇷**

