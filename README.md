# 🧠 pysm — A Simple Python Assembly Interpreter

`pysm` is a lightweight assembly-like virtual machine written in Python. It supports a range of basic instructions, labels, syscalls, and memory/register manipulation — perfect for learning how interpreters or virtual CPUs work.

---

## 🚀 How to Run

Run an assembly program with:

```bash
python3 vm.py examples/hello.asm
```

---

## 🐞 Debug Mode

To run the interpreter in debug mode (prints registers, memory, and instruction each step):

```bash
python3 vm.py examples/hello.asm --debug
```

---

## 🧩 Passing Arguments

You can pass arguments to your assembly program using:

```bash
python3 vm.py examples/echo.asm arg1 arg2 ...
```

Each argument is accessible as `arg1`, `arg2`, etc. from inside the program.

---

## 🧾 Supported Instructions

| Instruction | Description |
| --- | --- |
| `mov a,b` | Move value `b` into `a` (register or variable) |
| `add a,b` | Add `b` to register `a` |
| `sub a,b` | Subtract `b` from register `a` |
| `mul a,b` | Multiply register `a` by `b` |
| `div a,b` | Divide register `a` by `b` (error on divide by 0) |
| `inc a` | Increment register `a` |
| `dec a` | Decrement register `a` |
| `cmp a,b` | Compare register `a` with value `b`, sets `cr` flag |
| `int a` | Convert the value in register `a` to an integer |
| `flt a` | Convert the value in register `a` to a float |
| `str a` | Convert the value in register `a` to a string |
| `var name,val` | Declare a variable with name and value |
| `nop` | Do nothing |
| `ret` | Ends a label block (used for `jl`) |
| `jl label` | Jump to label and execute it as a function |
| `jlt label` | Jump to label **if** comparison flag `cr` is `True` |
| `jlf label` | Jump to label **if** comparison flag `cr` is `False` |
| `jmp line` | Unconditionally jump to a specific line number |
| `jt line` | Jump if `cr == True` |
| `jf line` | Jump if `cr == False` |
| `load rX` | Load value from memory at `dp` into `rX` |
| `store rX` | Store value of `rX` into memory at `dp` |

---

## 🧠 Registers

| Register | Purpose |
| --- | --- |
| `r1`–`r5` | General-purpose registers |
| `ar1`–`ar5` | Argument registers for syscalls |
| `frr` | Return/output register (e.g., stores syscall output) |
| `scr` | Holds syscall number |
| `cr` | Comparison result flag (`True` or `False`) |
| `dp` | Data pointer used for `load`/`store` |

---

## 📞 Syscalls

Trigger with:

```asm
mov scr, <code>
sys
```

| Code | Effect |
| --- | --- |
| `10` | Print value in `ar1` |
| `15` | Input prompt in `ar1`, store result in `frr` |
| `20` | Exit with code in `frr` |
| `25` | File read/write (`ar1`: path, `ar2`: mode, `ar3`: data) |
| `30` | Execute code in `ar1` as Python |
| `35` | Random integer between `ar1` and `ar2` → `frr` |
| `50` | Random choice from `ar1`–`ar5` → `frr` |
| `55` | Reset all registers to 0/default |
| `60` | Clear all user-defined variables |
| `65` | Panic with message in `ar1` |
| `70` | Store current program counter in `frr` |
| `75` | Pick random non-zero memory value → `frr` |

---

## 📂 Examples

See the [`examples/`](examples/) folder for ready-to-run programs:

-   `hello.asm` – Print "Hello, World!"
    
-   `input_echo.asm` – Ask user for input and respond
    
-   `infinite_loop_counter.asm` – Count upward forever, printing each value
    

---

## 🧪 Status

> 🚧 Actively developed — feedback, issues, and contributions welcome!

---
