# SMALL

This is a tiny lil language for my Comp project. It has the following syntax:

```ABNF
program = *(identifier "{" *statement "}")
identifier = *VCHAR
integer = *DIGIT
string = DQUOTE *(VCHAR / SP / NL / CR) DQUOTE
statement = push / pop / get / set / call / ret / putc / getc / let / if
push  = string / identifier / integer
pop   = "pop"
get   = "get"
set   = "set"
call  = "call"
putc  = "putc"
getc  = "getc"
let   = "let" identifier "at" integer
if    = "ifthen" "{" *statement "}"
while = "while" "{" "}"
```

And thus has the following lexical tokens:

- identifier
- integer
- string
- `{`
- `}`
- `pop`
- `get`
- `set`
- `call`
- `putc`
- `getc`
- `let`
- `at`
- `ifthen`
- `while`

It will be compiled to the following bytecode:

```
-OPCODE-----name-----------arguments------
| 0x00 | push        | imm8              |
| 0x01 | pushx       | immX              |
| 0x02 | drop        | imm8              |
| 0x03 | call        |      [x]          |
| 0x04 | callz       |      [8] [x]      |
| 0x05 | ret         |      [x]          |
| 0x06 | retz        |      [8] [x]      |
| 0x07 | get         |      [x]          |
| 0x08 | set         |      [8] [x]      |
| 0x09 | out         |      [8]          |
| 0x0A | in          |      [8]          |
| 0x0B | newstack    |                   |
| 0x0C | laststack   |                   |
------------------------------------------
