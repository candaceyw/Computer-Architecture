"""CPU functionality."""

# hlt halts the program
# ldi load immediate
# prn print
# load "immediate", stores a value in a reg, or set this reg to this value

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0  # program counter
        self.sp = 7

        self.running = False

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print('Usage: ls8.py "program name"')
            sys.exit(1)

        try:
            with open(f'examples/{sys.argv[1]}') as f:
                for line in f:
                    # ignore hashtag
                    comment_split = line.split('#')
                    # .strip() will get rid of any spaces
                    num = comment_split[0].strip()
                    if num == "":
                        continue
                    # convert binary string to integer
                    value = int(num, 2)
                    self.ram_write(address, value)

                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]
        #
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        HLT = 0b00000001
        PRN = 0b01000111
        MUL = 0b10100010
        POP = 0b01000110
        PUSH = 0b01000101

        running = True

        while running:

            # Instruction Register
            instruction = self.ram_read(self.pc)
            # sp = self.sp

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == HLT:
                self.running = False
                self.pc += 1

            elif instruction == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif instruction == MUL:  # --> Multiply the values  using ALU
                # print('MUL')
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3

            elif instruction == PRN:
                val = self.ram[self.pc + 1]
                print(self.reg[val])
                self.pc += 2

            elif instruction == PUSH:
                # reg == 1st argument
                reg = self.ram[self.pc + 1]
                # grab the values we are putting on the reg
                val = self.reg[reg]
                # Decrement the SP
                self.reg[self.sp] -= 1
                # Copy/write value in given register to address pointed to by SP
                self.ram[self.reg[self.sp]] = val
                # Increment PC by 2
                self.pc += 2

            elif instruction == POP:
                reg = self.ram[self.pc + 1]  # memory of the register holding our SP
                val = self.ram[self.reg[self.sp]]  # register number 7
                self.reg[reg] = val  # copy that value into register that we are pointing at
                self.reg[self.sp] += 1  # incrememnt the stock pointer:
                # print(val)
                self.pc += 2

            # else:
            #     print(f"Unknown instruction {instruction}")
            #     sys.exit(1)
