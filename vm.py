class RegisterError(Exception):pass
class BoundsError(Exception):pass
class OpcodeError(Exception):pass
class FileError(Exception):pass
try:
    import random
    import argparse
    import shlex
    from time import sleep

    def panic(message):
        print(f"on line {program_counter + 1}")
        print(message)
        exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file to interpret")
    parser.add_argument("--debug", action="store_true", help="enable debug mode")
    parser.add_argument("args", nargs="*", help="args to pass to the assembly")

    args = parser.parse_args()
    PATH = args.file
    debug = args.debug

    # Program args are in args.args
    program_vars = {
        f"arg{i}": val for i, val in enumerate(args.args, 1)
    }
    def split_commas_keep_quotes(s):
        lexer = shlex.shlex(s, posix=True)
        lexer.whitespace = ','
        lexer.whitespace_split = True
        lexer.commenters = ''
        return list(lexer)


    program_mem = [0 for _ in range(50)]

    labels = {}

    def handle_label():
        global code
        new_code = []
        current_label = None
        for line in code:
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            line = line.split(";")[0].strip()
            if not line:
                continue
            if line.endswith(":"):
                current_label = line[:-1]
                labels[current_label] = []
            elif current_label:
                if line == "ret":
                    current_label = None
                else:
                    labels[current_label].append(line)
            else:
                new_code.append(line)
        code = new_code


    registers = {
        "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0,
        "frr": 0, "scr": 0,
        "ar1": 0, "ar2": 0, "ar3": 0, "ar4": 0, "ar5": 0,
        "cr": False,
        "dp":0
    }

    def parse_value(val:str):
        if val in registers:
            return registers[val]
        if val.startswith('"') and val.endswith('"'):
            return val[1:-1]
        if val in program_vars:
            return program_vars[val]
        try:
            return int(val)
        except ValueError:
            return val

    def execute(instruction: str) -> None:
        global program_counter, registers
        instruction = instruction.strip()
        if not instruction or instruction.startswith(";"):
            return
        instruction = instruction.split(";")[0].strip()
        if not instruction:
            return
        parts = instruction.split(" ", 1)
        opcode = parts[0]
        args = split_commas_keep_quotes(parts[1]) if len(parts) > 1 else []
        if opcode == "mov":
            dest = args[0]
            src = args[1]
            if dest in registers:
                registers[dest] = parse_value(src)
            else:
                raise RegisterError("tried to move a value into a non register")
        elif opcode == "add":
            if args[0] in registers:
                registers[args[0]] += parse_value(args[1])
        elif opcode == "sub":
            if args[0] in registers:
                registers[args[0]] -= parse_value(args[1])
        elif opcode == "mul":
            if args[0] in registers:
                registers[args[0]] *= parse_value(args[1])
        elif opcode == "div":
            divisor = parse_value(args[1])
            if divisor == 0:
                raise ZeroDivisionError("division by 0")
            if args[0] in registers:
                registers[args[0]] = registers[args[0]] / divisor
        elif opcode == "nop":
            pass
        elif opcode == "sys":
            handle_syscall(registers["scr"])
        elif opcode == "int":
            if args[0] in registers:
                registers[args[0]] = int(registers[args[0]])
        elif opcode == "cmp":
            if args[0] not in registers:
                raise RegisterError("trying to compare with a non register")
            registers["cr"] = (registers[args[0]] == parse_value(args[1]))
        elif opcode == "jt":
            if int(args[0]) >= len(code):
                raise BoundsError("out of bounds jump")
            if registers["cr"]:
                program_counter = int(args[0])
        elif opcode == "jf":
            if not registers["cr"]:
                if int(args[0]) >= len(code):
                    raise BoundsError("out of bounds jump")
                program_counter = int(args[0])
        elif opcode == "jmp":
            if int(args[0]) >= len(code):
                raise BoundsError("out of bounds jump")
            program_counter = int(args[0])
        elif opcode == "inc":
            if args[0] in registers:
                registers[args[0]] += 1
        elif opcode == "dec":
            if args[0] in registers:
                registers[args[0]] -= 1
        elif opcode == "var":
            program_vars[args[0]] = parse_value(args[1])
        elif opcode == "load":
            if args[0] not in registers:
                raise RegisterError("tried to load value into non register")
            if registers["dp"] >= len(program_mem):
                raise MemoryError("tried to load invalid memmory adress")
            registers[args[0]] = program_mem[registers["dp"]]
        elif opcode == "store":
            if registers["dp"] >= len(program_mem):
                raise MemoryError("tried to write to invalid memmory")
            if args[0] not in registers:
                raise RegisterError("tried to store into invalid register")
            program_mem[registers["dp"]] = registers[args[0]]
        elif opcode == "str":
            registers[args[0]] = str(registers[args[0]])
        elif opcode == "jl":
            for instruction in labels[args[0]]:
                execute(instruction)
        elif opcode == "jlt":
            if registers["cr"]:
                for instruction in labels[args[0]]:
                    execute(instruction)
        elif opcode == "jlf":
            
            if not registers["cr"]:
                for instruction in labels[args[0]]:
                    execute(instruction)
        elif opcode == "flt":
            registers[args[0]] = float(registers[args[0]])
        else:
            raise OpcodeError("uknown opcode")

    def handle_syscall(call):
        global registers,program_vars
        if call == 10:
            print(registers["ar1"],end="")
        elif call == 15:
            registers["frr"] = input(str(registers["ar1"]))
        elif call == 20:
            exit(int(registers["frr"]))
        elif call == 25:
            with open(str(registers["ar1"]).strip(), str(registers["ar2"]).strip()) as f:
                if registers["ar2"].strip() == "r":
                    registers["frr"] = f.read()
                elif registers["ar2"].strip() == "w":
                    f.write(str(registers["ar3"]))
                else:

                    raise FileError("Invalid file mode: only 'r' or 'w' supported")
        elif call == 30:
            exec(str(registers["ar1"]))
        elif call == 35:
            registers["frr"] = random.randint(int(registers["ar1"]), int(registers["ar2"]))
        elif call == 50:
            registers["frr"] = random.choice([
                registers["ar1"], registers["ar2"], registers["ar3"],
                registers["ar4"], registers["ar5"]
            ])
        elif call == 75:
            for _ in range(100):
                registers["frr"] = random.choice(program_mem)
                if registers["frr"] != 0:
                    break
            else:
                raise MemoryError("could not find non-zero memory value")
        elif call == 55:
            registers = {
        "r1": 0, "r2": 0, "r3": 0, "r4": 0, "r5": 0,
        "frr": 0, "scr": 0,
        "ar1": 0, "ar2": 0, "ar3": 0, "ar4": 0, "ar5": 0,
        "cr": False,
        "dp":0
    }
        elif call == 60:
            program_vars = {}
        elif call == 65:
            panic(registers["ar1"])
        elif call == 70:
            registers["frr"] = program_counter
        else:
            raise SystemError(f"Unknown syscall code: {call}")


    iterations = 0
    # Main loop
    with open(PATH, "r") as f:
        code = f.readlines()
    for i in range(len(code)):
        code[i] = code[i].encode('utf-8').decode('unicode_escape')
    program_counter = 0
    handle_label()
    while True: #changed so now to exit you have to move your exit value to frr and then 20 into scr and then sys
        try:
            registers["dp"] = int(registers["dp"])
            old_pc = program_counter
            if program_counter >= len(code):
                raise BoundsError("program_counter out of bounds")
            execute(code[program_counter])
            if debug:
                print("-" * 40)
                print(f"PC: {program_counter}")
                print(f"Instruction: {code[program_counter].strip()}")
                print("Registers:")
                for k, v in registers.items():
                    print(f"  {k:>4}: {v}")
                if program_vars:
                    print("Variables:")
                    for k, v in program_vars.items():
                        print(f"  {k}: {v}")
                print("mem: ")
                for thing in program_mem:
                    print(f"{thing}\n") if not thing == 0 else None
                print("-" * 40)
                sleep(0.1)
            if program_counter == old_pc:
                program_counter += 1
        except RecursionError:
            continue
except KeyboardInterrupt:pass
