
import logging
import time
from itertools import permutations
from queue import Queue
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


def get_data(loc):
    with open(loc) as f:
        rawdata = f.read().split(',')
    return list(map(int,rawdata))        
class Amplifier:
    def __def__(self, program_location, phase_setting):
        self.inputs = Queue()
        self.inputs.put(phase_setting)
        self.output = None
        self.pointer = 0
        self.intcode_program = get_data(program_location)
        self.halted = False
        self.iteration = 0
    def run_program(self):
        while True:
            self.iteration += 1
            if self.pointer >=len(self.intcode_program)-1:
                raise Exception(f"Pointer at end of program, pointer:{self.pointer}, program length: {len(self.intcode_program)}")
            opcode_to_process = self.intcode_program[self.pointer]
            if opcode_to_process%100 == 99:
                logging.debug(f"Program halted without error after {self.iteration} iterations")
                self.halted = True
                return
            # print(f"Iteration {iteration}, pointer:{pointer}, opcode:{opcode_to_process}")
            # print(intcode_program[pointer:pointer+4])
            arg1,arg2=None,None
            p1,p2,p3=None,None,None
            p1 = self.intcode_program[self.pointer+1]
            if opcode_to_process % 100 not in [3,4]:
                p2 = self.intcode_program[self.pointer+2]
            if opcode_to_process % 100 in [1,2,7,8]:
                p3 = self.intcode_program[self.pointer+3]
            if opcode_to_process > 99:
                opcode = opcode_to_process % 100
                mode1 = opcode_to_process // 100 % 10
                mode2 = opcode_to_process // 1000 % 10
                if mode1==0: #position mode
                    arg1 = self.intcode_program[p1]
                else: #immediate mode
                    arg1 = p1
                if mode2==0 and opcode in [1,2,5,6,7,8]: # position mode (3 and 4 don't use position mode)
                    arg2 = self.intcode_program[p2]
                else: #immediate mode
                    arg2 = p2
            else:
                opcode = opcode_to_process
                arg1 = self.intcode_program[p1]
                if opcode in [1,2,5,6,7,8]:
                    arg2 = self.intcode_program[p2]

            if opcode == 1:
                self.intcode_program[p3] = arg1 + arg2
                pointer += 4
            elif opcode == 2:
                self.intcode_program[p3] = arg1 * arg2
                pointer += 4
            elif opcode == 3:
                self.intcode_program[p1] = self.inputs.put()
                pointer += 2
            elif opcode == 4:
                self.output.append(arg1)
                pointer += 2
                return
            elif opcode == 5:
                if arg1 != 0:
                    pointer = arg2
                else:
                    pointer += 3
            elif opcode == 6:
                if arg1 == 0:
                    pointer = arg2
                else:
                    pointer += 3
            elif opcode == 7:
                if arg1 < arg2:
                    self.intcode_program[p3] = 1
                else:
                    self.intcode_program[p3] = 0
                pointer += 4
            elif opcode == 8:
                if arg1 == arg2:
                    self.intcode_program[p3] = 1
                else:
                    self.intcode_program[p3] = 0
                pointer += 4
            else:
                raise Exception(f"Unknown opcode:{opcode} on iteration {self.iteration}")

sequence=[9,8,7,6,5]
program_location = './data/day7.txt'
[Amplifier(program_location, phase_setting) for phase_setting in sequence]