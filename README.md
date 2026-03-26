# Spine64

A custom assembly language compiler targeting x86-64.

## Overview

Spine64 provides a NASM-like syntax for writing x86-64 assembly. It parses `.s64` source files and generates machine code.

## Language Features

- **Modules**: Organize code into `data`, `reserve`, and `code` sections
- **Functions**: Define with `fn global`, `fn raw`, or `fn`
- **Interrupt Handlers**: Handle hardware interrupts with `on interrupt N`
- **Aliases**: Map symbolic names to registers

## Registers

| Name | Purpose |
|------|---------|
| `r1`-`r4` | General purpose |
| `ret` | Return value |
| `stp` | Stack pointer |
| `f1`, `f2` | Floating point |
| `src`, `dst`, `cnt` | Memory operations |

## Example

```asm
origin 0x7C00

module code
    fn global main
    start
        move counter 10
        call add_two
        halt
    end
end
```

## Building

```bash
python lexer.py source.s64   # Tokenize
python parser.py source.s64   # Parse to AST
python codegen.py source.s64  # Generate binary
```

## License

MIT
