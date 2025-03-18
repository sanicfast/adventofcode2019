def get_data(loc):
    with open(loc) as f:
        rawdata = f.read().split(',')
    return list(map(int,rawdata))



intcode_program = get_data("./data/day5.txt")

pointer = 0
inputs=[1]
output =[]
while True:
    opcode_to_process = intcode_program[pointer]
    if opcode_to_process > 99:
        opcode = opcode_to_process % 100
        mode1 = opcode_to_process // 100 % 10
        mode2 = opcode_to_process // 1000 % 10
    else:
        opcode = opcode_to_process


    if opcode == 99:
        break
    elif opcode == 1:
        # add them
        pointer += 4
    elif opcode == 2:
        # multiply them
        pointer += 4
    elif opcode == 3:
        index = intcode_program[pointer+1]
        intcode_program[index] = inputs.pop()
        pointer += 2
    elif opcode == 4:
        index = intcode_program[pointer+1]
        output.append(intcode_program[index])
        pointer += 2
    else:
        raise Exception("Unknown opcode")
