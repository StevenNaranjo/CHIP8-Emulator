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

---

### S   
- **Stack**: A data structure that follows the Last In, First Out (LIFO) principle. It is used to store return addresses, function calls, or local variables, and is manipulated with push and pop operations.

---

**Built with ❤️ by Alex Naranjo**  
**Costa Rica 🇨🇷**

