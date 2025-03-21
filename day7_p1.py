
import logging
import time
from itertools import permutations
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)


def get_data(loc):
    with open(loc) as f:
        rawdata = f.read().split(',')
    return list(map(int,rawdata))        

def run_program(program_location, inputs):
    intcode_program = get_data(program_location)
    pointer = 0
    output =[]
    iteration=0
    while True:
        iteration += 1
        if pointer >=len(intcode_program)-1:
            raise Exception(f"Pointer at end of program, pointer:{pointer}, program length: {len(intcode_program)}")
        opcode_to_process = intcode_program[pointer]
        if opcode_to_process%100 == 99:
            logging.debug(f"Program halted without error after {iteration} iterations")
            break
        # print(f"Iteration {iteration}, pointer:{pointer}, opcode:{opcode_to_process}")
        # print(intcode_program[pointer:pointer+4])
        arg1,arg2=None,None
        p1,p2,p3=None,None,None
        p1 = intcode_program[pointer+1]
        if opcode_to_process % 100 not in [3,4]:
            p2 = intcode_program[pointer+2]
        if opcode_to_process % 100 in [1,2,7,8]:
            p3 = intcode_program[pointer+3]
        if opcode_to_process > 99:
            opcode = opcode_to_process % 100
            mode1 = opcode_to_process // 100 % 10
            mode2 = opcode_to_process // 1000 % 10
            if mode1==0: #position mode
                arg1 = intcode_program[p1]
            else: #immediate mode
                arg1 = p1
            if mode2==0 and opcode in [1,2,5,6,7,8]: # position mode (3 and 4 don't use position mode)
                arg2 = intcode_program[p2]
            else: #immediate mode
                arg2 = p2
        else:
            opcode = opcode_to_process
            arg1 = intcode_program[p1]
            if opcode in [1,2,5,6,7,8]:
                arg2 = intcode_program[p2]
        # if type(arg1) == list or type(arg2)==list:
        #     breakpoint()
        if opcode == 1:
            intcode_program[p3] = arg1 + arg2
            pointer += 4
        elif opcode == 2:
            intcode_program[p3] = arg1 * arg2
            pointer += 4
        elif opcode == 3:
            intcode_program[p1] = inputs.pop()
            pointer += 2
        elif opcode == 4:
            output.append(arg1)
            pointer += 2
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
                intcode_program[p3] = 1
            else:
                intcode_program[p3] = 0
            pointer += 4
        elif opcode == 8:
            if arg1 == arg2:
                intcode_program[p3] = 1
            else:
                intcode_program[p3] = 0
            pointer += 4
        else:
            raise Exception(f"Unknown opcode:{opcode} on iteration {iteration}")
    return output

def try_sequence_p1(sequence,program_location):
    output=[0]
    sequence.reverse()
    while sequence:
        logging.debug(f'output:{output}, sequence:{sequence}')
        if len(output)!=1:
            raise Exception(f"Output is not a single value, output:{output}")
        inputs = [output[0],sequence.pop()]
        logging.debug(inputs)
        output=run_program(program_location, inputs)
    return output[0]

def p1():
    program_location = './data/day7.txt'
    max_val = 0
    for sequence in map(list,permutations(range(5))):
        output = try_sequence_p1(sequence,program_location)
        max_val = max(output,max_val)
    print('Part 1:',max_val)
p1()

