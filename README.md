# Bynary

Making your life easier

why giving computer instructions via a Compilar, while you can just do it directly?

just write it in binary 

made by using Python.

## Usage

BYNARY programs are written in binary bytes.
Each byte is split into two parts:

-First 4 bits → instruction

-Last 4 bits → register number

**Instruction**
```
Basic (0xxx):

0000 NOOP
0001 LOAD value
0010 ADD (increment)
0011 SUB (decrement)
0100 PRINT (number with newline)
0101 COPY (reg to reg)
0110 JNZ (jump if not zero)
0111 JMP (unconditional jump)

Math & I/O (1xxx):

1000 END
1001 PRINTC (character)
1010 INPUT (character)
1011 ADDR (add registers)
1100 SUBR (subtract registers)
1101 MULR (multiply registers)
1110 DIVR (divide registers)

Extended ops (1111 + next byte):

1111 00000000 - MOD (modulo)
1111 00000001 - CMP (compare, returns -1/0/1)
1111 00000010 - STORE (to memory)
1111 00000011 - LOAD_MEM (from memory)
1111 00000100 - JZ (jump if zero)
1111 00000101 - JLT (jump if negative)
1111 00000110 - AND (bitwise)
1111 00000111 - OR (bitwise)
1111 00001000 - XOR (bitwise)
1111 00001001 - SHL (shift left)
1111 00001010 - SHR (shift right)
1111 00001011 - PRINTN (no newline)
1111 00001100 - INPUTN (number input)
```

### How to get "Hello"
```
00010000
01101000
10010000

00010000
01100101
10010000

00010000
01101100
10010000

00010000
01101100
10010000

00010000
01101111
10010000

10000000
```

**Output**
```
hello
```
