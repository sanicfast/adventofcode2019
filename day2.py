def get_data(loc):
    with open(loc) as f:
        rawdata = f.read().split(',')
    return list(map(int,rawdata))

# 1, 2, or 99. 
# opcode 99 means that the program is finished
# Opcode 1 adds together numbers read from two positions and stores the result 
# in a third position. The three integers immediately after the opcode tell you 
# these three positions - the first two indicate the positions from which you 
# should read the input values, and the third indicates the position at which the 
# output should be stored.
# 

def run_program(noun,verb):
    def one(p1,p2,p3):
        intcode_program[p3] = intcode_program[p1] + intcode_program[p2]
    def two(p1,p2,p3):
        intcode_program[p3] = intcode_program[p1] * intcode_program[p2]

    intcode_program = get_data("./data/day2.txt")
    intcode_program[1] = noun
    intcode_program[2] = verb

    pointer = 0
    while True:
        opcode = intcode_program[pointer]
        if opcode == 99:
            break
        elif opcode == 1:
            one(intcode_program[pointer+1],intcode_program[pointer+2],intcode_program[pointer+3])
        elif opcode == 2:
            two(intcode_program[pointer+1],intcode_program[pointer+2],intcode_program[pointer+3])
        else:
            raise Exception("Unknown opcode")
        pointer += 4
    return intcode_program[0]

print('part 1: ',run_program(12,2))
for noun in range(100):
    for verb in range(100):
        if run_program(noun,verb) == 19690720:
            print('part 2: ',100 * noun + verb)
            break
    else:
        continue
    break
print('done')