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
0000 NOOP      do nothing
0001 LOAD      load value into register (next byte = value)
0010 ADD       add 1 to register
0011 SUB       subtract 1 from register
0100 PRINT     print number
1001 PRINTC    print character (ASCII)
0110 JNZ       jump if register not zero
0111 JMP       jump always
1000 END       stop program
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
