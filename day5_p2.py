def get_data(loc):
    with open(loc) as f:
        rawdata = f.read().split(',')
    return list(map(int,rawdata))



intcode_program = get_data("./data/day5.txt")
# intcode_program = get_data("./data/day5_ex.txt")

# 99 - halt, 0 parameters
# 3 - input, 1 parameter
# 4 - output, 1 parameter
# 5 - jump-if-true, 2 parameters
# 6 - jump-if-false, 2 parameters
# 1 - add, 3 parameters
# 2 - multiply, 3 parameters
# 7 - less than, 3 parameters
# 8 - equals, 3 parameters




pointer = 0
inputs=[5]
output =[]
iteration=0
while True:
    iteration += 1
    if pointer >=len(intcode_program)-1:
        raise Exception(f"Pointer at end of program, pointer:{pointer}, program length: {len(intcode_program)}")
    opcode_to_process = intcode_program[pointer]
    if opcode_to_process%100 == 99:
        print(f"Program halted without error after {iteration} iterations")
        break
    # print(f"Iteration {iteration}, pointer:{pointer}, opcode:{opcode_to_process}")
    # print(intcode_program[pointer:pointer+4])
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

print(output)