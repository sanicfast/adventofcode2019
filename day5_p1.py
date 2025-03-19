def get_data(loc):
    with open(loc) as f:
        rawdata = f.read().split(',')
    return list(map(int,rawdata))



intcode_program = get_data("./data/day5.txt")
# intcode_program = get_data("./data/day5_ex.txt")

pointer = 0
inputs=[1]
output =[]
iteration=0
while True:
    # print(f"Iteration: {iteration}, Pointer: {pointer}")
    # print(intcode_program[pointer:pointer+5])
    iteration += 1
    if pointer >=len(intcode_program)-1:
        raise Exception(f"Pointer at end of program, pointer:{pointer}, program length: {len(intcode_program)}")
    opcode_to_process = intcode_program[pointer]
    if opcode_to_process == 99:
        break
    p1 = intcode_program[pointer+1]
    p2 = intcode_program[pointer+2]
    p3 = intcode_program[pointer+3]
    if opcode_to_process > 99:
        opcode = opcode_to_process % 100
        mode1 = opcode_to_process // 100 % 10
        mode2 = opcode_to_process // 1000 % 10
        if mode1==0: #position mode
            arg1 = intcode_program[p1]
        else: #immediate mode
            arg1 = p1
        if mode2==0 and opcode < 3: # position mode
            arg2 = intcode_program[p2]
        else: #immediate mode
            arg2 = p2
    else:
        opcode = opcode_to_process
        arg1 = intcode_program[p1]
        if opcode < 3:
            arg2 = intcode_program[p2]


    if opcode == 99:
        break
    elif opcode == 1:
        intcode_program[p3] = arg1 + arg2
        pointer += 4
    elif opcode == 2:
        intcode_program[p3] = arg1 * arg2
        pointer += 4
    elif opcode == 3:
        index = intcode_program[pointer+1]
        intcode_program[index] = inputs.pop()
        pointer += 2
    elif opcode == 4:
        # if arg1 != 0:
        #     breakpoint()
        output.append(arg1)
        pointer += 2
    else:
        raise Exception(f"Unknown opcode:{opcode}")

print(output)