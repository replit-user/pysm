# 🧠 `pysm` — A Python Assembly-Style Virtual Machine

**`pysm`** is a lightweight Python-based virtual machine that interprets a custom assembly-like language. It’s designed for learning and experimenting with low-level instruction sets, virtual registers, and system call-style interactions — all inside a Python script.

---

## 📦 Features

-   Custom assembly instruction set
    
-   Virtual CPU with 16+ registers
    
-   Label-based control flow (like functions)
    
-   Simulated memory and syscalls
    
-   Error handling and debug mode
    
-   Program arguments and variable support
    

---

## 🚀 Getting Started

### ▶️ Run a Program

```bash
python3 main.py examples/hello.asm
```

### 🐞 Enable Debug Mode

```bash
python3 main.py examples/hello.asm --debug
```

This prints the current instruction, registers, memory, and variables on each step (with delay).

### 🧩 Pass Program Arguments

```bash
python3 main.py examples/input.asm user123
```

Inside your `.asm` file, arguments are available as:

-   `arg1`, `arg2`, `arg3`, ...
    

---

## 🔠 Instruction Set

| Instruction | Description |
| --- | --- |
| `mov a,b` | Move value `b` into `a` |
| `add a,b` | Add `b` to register `a` |
| `sub a,b` | Subtract `b` from register `a` |
| `mul a,b` | Multiply register `a` by `b` |
| `div a,b` | Divide register `a` by `b` |
| `inc a` | Increment register `a` |
| `dec a` | Decrement register `a` |
| `cmp a,b` | Set `cr` if `a == b` |
| `cmplt a,b` | Set `cr` if `a < b` |
| `cmpgt a,b` | Set `cr` if `a > b` |
| `int a` | Convert value in `a` to integer |
| `flt a` | Convert value in `a` to float |
| `str a` | Convert value in `a` to string |
| `nop` | Do nothing |
| `var name,val` | Declare variable |
| `load rX` | Load from memory at `dp` into `rX` |
| `store rX` | Store `rX` into memory at `dp` |
| `jl label` | Jump and run label block |
| `jlt label` | Jump to label if `cr == True` |
| `jlf label` | Jump to label if `cr == False` |
| `jmp n` | Jump to absolute line `n` |
| `jt n` | Jump to line `n` if `cr == True` |
| `jf n` | Jump to line `n` if `cr == False` |
| `ret` | End of label block |

---

## 🧠 Registers

| Name | Purpose |
| --- | --- |
| `r1`–`r5` | General-purpose registers |
| `ar1`–`ar5` | Argument registers for syscalls |
| `frr` | Return/result register |
| `scr` | Syscall selector |
| `cr` | Comparison result (True/False) |
| `dp` | Memory data pointer |

## 📞 System Calls (`sys`)
System calls are invoked using the special `sys` instruction after setting up the appropriate syscall number in the `scr` register. Depending on the syscall, values must be passed in the argument registers (`ar1`, `ar2`, `ar3`, etc.), and results are typically returned in the `frr` register.

### 🔢 Usage Pattern

```asm
mov ar1, <value1>
mov ar2, <value2>
...
mov scr, <syscall_number>
sys
```

---

### `10` — Print a value

**Description:** Outputs the value in `ar1` to standard output. No newline is added automatically.

**Usage:**

```asm
mov ar1, "Hello"
mov scr, 10
sys
```

---

### `15` — Input prompt

**Description:** Prompts the user with the string in `ar1`, waits for input, and stores the result in `frr`.

**Usage:**

```asm
mov ar1, "Enter your name: "
mov scr, 15
sys
mov r1, frr ; Store input in r1
```

---

### `20` — Exit program

**Description:** Terminates the program using the exit code in `frr`. Optionally prints a message based on the code.

**Accepted codes:**

-   `0`: Success
    
-   `1`: Error occurred
    
-   `5`: Program ended early
    
-   `10`: Program caught a custom error
    

**Usage:**

```asm
mov frr, 0 ; exit code
mov scr, 20
sys
```

---

### `25` — File read/write

**Description:** Performs basic file I/O.

-   `ar1`: File path (e.g., `"file.txt"`)
    
-   `ar2`: Mode — `"r"` to read, `"w"` to write
    
-   `ar3`: Data to write (only used in write mode)
    
-   `frr`: Contains file content after reading
    

**Read Example:**

```asm
mov ar1, "note.txt"
mov ar2, "r"
mov scr, 25
sys
mov r1, frr ; file contents → r1
```

**Write Example:**

```asm
mov ar1, "out.txt"
mov ar2, "w"
mov ar3, "data to save"
mov scr, 25
sys
```

---

### `30` — Execute Python code

**Description:** Interprets the string in `ar1` as Python code using `exec()`.

**Usage:**

```asm
mov ar1, "print('Hello from Python')"
mov scr, 30
sys
```

---

### `35` — Random integer

**Description:** Generates a random integer between `ar1` and `ar2`, inclusive, and stores the result in `frr`.

**Usage:**

```asm
mov ar1, 1
mov ar2, 10
mov scr, 35
sys
mov r1, frr ; Random value between 1 and 10
```

---

### `50` — Random choice from args

**Description:** Randomly selects one value from the registers `ar1`–`ar5` and stores it in `frr`.

**Usage:**

```asm
mov ar1, 100
mov ar2, 200
mov ar3, 300
mov scr, 50
sys
mov r1, frr
```

---

### `55` — Reset all registers

**Description:** Clears all general-purpose and syscall registers (sets them to `0` or `False`).

**Usage:**

```asm
mov scr, 55
sys
```

---

### `60` — Clear all variables

**Description:** Deletes all variables previously created with the `var` instruction or argument inputs.

**Usage:**

```asm
mov scr, 60
sys
```

---

### `65` — Panic and crash

**Description:** Immediately prints an error message from `ar1` and terminates the program with a stack trace.

**Usage:**

```asm
mov ar1, "Something went wrong!"
mov scr, 65
sys
```

---

### `67` — Raise custom error

**Description:** Manually raises an exception of a given type with a message.  
`ar1` = error type code, `ar2` = message

| Code | Exception Raised |
| --- | --- |
| `1` | `OpcodeError` |
| `2` | `BoundsError` |
| `3` | `ExitCodeError` |
| `4` | `FileError` |
| `5` | `MemoryError` |
| `6` | `SystemError` |

**Usage:**

```asm
mov ar1, 1 ; OpcodeError
mov ar2, "invalid opcode encountered"
mov scr, 67
sys
```

---

### `70` — Save program counter

**Description:** Stores the current line number (`program_counter`) in `frr`.

**Usage:**

```asm
mov scr, 70
sys
mov r1, frr ; store PC
```

---

### `75` — Random non-zero memory value

**Description:** Picks a random non-zero value from `program_mem` and stores it in `frr`. Fails if all memory is zero.

**Usage:**

```asm
mov scr, 75
sys
mov r1, frr
```

---

### `80` — Random float

**Description:** Generates a random float between `0` and `1` and stores it in `frr`.

**Usage:**

```asm
mov scr, 80
sys
mov r1, frr
```

---

## 💾 Memory

-   `program_mem` — 50 integer memory cells
    
-   Use `dp` to select index
    
-   Use `load` and `store` to read/write memory
    

---

## 📁 Example Programs

Stored in [`examples/`](examples/):

### 📢 `hello.asm`

```asm
mov ar1, "Hello, World!\n"
mov scr, 10
sys
mov frr, 0
mov scr, 20
sys
```

### 🔁 `loop.asm`

```asm
mov r1,0
loop:
inc r1
mov ar1,r1
mov scr,10
sys
mov ar1,"\n"
sys
jl loop
ret
jl loop
```

### 👤 `input.asm`

```asm
print:
mov scr,10
sys
ret

input:
mov scr,15
sys
ret

mov ar1,"what is your name:\t"
jl input
mov r1,frr
mov ar1,"Hello, "
jl print
mov ar1,r1
jl print
mov ar1,"!\n"
jl print
mov scr,20
mov frr,0
sys
```

---

## 🛠 Development

> 🧪 Actively maintained — bug reports and contributions welcome!

-   Written in a single Python file (`main.py`)
    
-   Easy to hack and modify
    
-   Minimal dependencies (only `argparse`, `shlex`, and `random`)
    

---

## ✅ Exit Codes

Exit is triggered via:

```asm
mov frr, <code>
mov scr, 20
sys
```

| Code | Meaning |
| --- | --- |
| `0` | Success |
| `1` | Generic error |
| `5` | Premature end |
| `10` | Program-caught error |

---

## 📜 License

MIT License — feel free to fork and modify.
