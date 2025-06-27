# 🧠 `pysm` — A Simple Python Assembly Interpreter

**`pysm`** is a lightweight, educational virtual machine written in Python that executes a custom assembly-like instruction set. It's perfect for learning how interpreters, virtual CPUs, and basic low-level systems work.

---

## 🚀 How to Run

Run an assembly program with:

```bash
python3 vm.py examples/hello.asm
```

---

## 🐞 Debug Mode

To enable debug mode (prints instruction, registers, memory, etc. every step):

```bash
python3 vm.py examples/hello.asm --debug
```

---

## 🧩 Passing Arguments

You can pass arguments to your assembly programs like so:

```bash
python3 vm.py examples/echo.asm hello world 123
```

Inside the program, these are available as:

-   `arg1`, `arg2`, `arg3`, ...
    

---

## 🧾 Supported Instructions

| Instruction | Description |
| --- | --- |
| `mov a,b` | Move value `b` into `a` (register or variable) |
| `add a,b` | Add `b` to register `a` |
| `sub a,b` | Subtract `b` from register `a` |
| `mul a,b` | Multiply register `a` by `b` |
| `div a,b` | Divide register `a` by `b` (error on divide-by-zero) |
| `inc a` | Increment register `a` |
| `dec a` | Decrement register `a` |
| `cmp a,b` | Compare `a` and `b`, store result in `cr` flag |
| `int a` | Convert value in `a` to integer |
| `flt a` | Convert value in `a` to float |
| `str a` | Convert value in `a` to string |
| `var name,val` | Declare variable `name` with value `val` |
| `nop` | Do nothing |
| `ret` | End label block |
| `jl label` | Jump to and execute label like a function |
| `jlt label` | Jump to label if `cr == True` |
| `jlf label` | Jump to label if `cr == False` |
| `jmp line` | Unconditional jump to line number |
| `jt line` | Jump to line if `cr == True` |
| `jf line` | Jump to line if `cr == False` |
| `load rX` | Load value from memory at `dp` into `rX` |
| `store rX` | Store value of `rX` into memory at `dp` |

---

## 🧠 Registers

| Register | Description |
| --- | --- |
| `r1`–`r5` | General-purpose registers |
| `ar1`–`ar5` | Argument registers for syscalls |
| `frr` | Syscall result register |
| `scr` | Syscall code register |
| `cr` | Condition flag (set by `cmp`) |
| `dp` | Data pointer for memory access |

---

## 📞 Syscalls

Triggered using:

```asm
mov scr, <code>
sys
```

| Code | Action |
| --- | --- |
| `10` | Print `ar1` (no newline) |
| `15` | Prompt with `ar1`, store input in `frr` |
| `20` | Exit with status in `frr` (`0`, `1`, `5`, or `10`) |
| `25` | File read/write (see below) |
| `30` | Execute Python code from `ar1` |
| `35` | Random int between `ar1` and `ar2` → `frr` |
| `50` | Random pick from `ar1`–`ar5` → `frr` |
| `55` | Reset all registers |
| `60` | Clear all program variables |
| `65` | Panic with message in `ar1` |
| `70` | Store current program counter in `frr` |
| `75` | Pick random non-zero value from memory → `frr` |

### File Syscall (`25`)

-   `ar1`: File path
    
-   `ar2`: Mode (`r`, `w`, `a`, `x`)
    
-   `ar3`: Content to write (only used in write modes)
    
-   `frr`: Will contain file content on read
    

---

## 💾 Memory

-   `program_mem`: 50 cells (0–49)
    
-   Use `dp` register to point to memory
    
-   Use `load` and `store` to read/write at `dp`
    

---

## 📂 Example Programs

Check the [`examples/`](examples/) folder:

-   `hello.asm` — Print “Hello, World!”
    
-   `input.asm` — take user's name and output a greeting
    
-   `loopr.asm` — Count and print forever
    

---

## 🧪 Development Status

> 🚧 Under active development — Contributions and feedback welcome!
