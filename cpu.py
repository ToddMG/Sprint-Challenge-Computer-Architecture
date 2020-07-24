"""CPU functionality"""

import sys

# Instructions
LDI = 0b10000010
CMP = 0b10100111
JEQ = 0b01010101
PRN = 0b01000111
JNE = 0b01010110
HLT = 0b00000001
JMP = 0b01010100


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.pc = 0
        self.running = True
        self.FL = 0b00000000

    def alu(self, instruction, reg1, reg2):
        if instruction == "CMP":
            self.FL &= 0b00000000
            if self.registers[reg1] == self.registers[reg2]:
                self.FL = 0b00000001
            elif self.registers[reg1] < self.registers[reg2]:
                self.FL = 0b00000100
            elif self.registers[reg1] > self.registers[reg2]:
                self.FL = 0b00000010
            self.pc += 3

    def hlt(self):
        self.running = False

    def jmp(self, reg_num):
        self.pc = self.registers[reg_num]

    def jeq(self, reg_num):
        if self.FL & 1 is 1:
            self.pc = self.registers[reg_num]
        else:
            self.pc += 2

    def jne(self, reg_num):
        if self.FL & 1 is 0:
            self.pc = self.registers[reg_num]
        else:
            self.pc += 2

    def ldi(self, reg_num, value):
        self.registers[reg_num] = value
        self.pc += 3

    def prn(self, reg_num):
        print(self.registers[reg_num])
        self.pc += 2

    def load(self):
        if len(sys.argv) < 2:
            print("Second filename expected, only one received. FORMAT: python cpu.py FILE")
            sys.exit()

        file_name = sys.argv[1]

        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()

                    if command == '':
                        continue

                    instruction = int(command, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file not found.')
            sys.exit()

    def run(self):
        self.load()
        while self.running:
            instruction = self.ram[self.pc]

            if instruction == CMP:
                reg1 = self.ram[self.pc + 1]
                reg2 = self.ram[self.pc + 2]
                self.alu("CMP", reg1, reg2)

            elif instruction == HLT:
                self.hlt()

            elif instruction == JMP:
                reg_num = self.ram[self.pc + 1]
                self.jmp(reg_num)

            elif instruction == JEQ:
                reg_num = self.ram[self.pc + 1]
                self.jeq(reg_num)

            elif instruction == JNE:
                reg_num = self.ram[self.pc + 1]
                self.jne(reg_num)

            elif instruction == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.ldi(reg_num, value)

            elif instruction == PRN:
                reg_num = self.ram[self.pc + 1]
                self.prn(reg_num)

            else:
                print(f"Instruction number {self.pc} not recognized!")
                self.pc += 1


if __name__ == "__main__":
    cpu = CPU()
    cpu.load()
    cpu.run()