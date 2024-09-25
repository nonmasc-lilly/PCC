"""
## Lexical tokens
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
"""

def lex(contents: str) -> list[tuple[str,str,int]]:
    i: int = 0;
    buf: str = "";
    ret: list[tuple[str,str]] = [];
    line: int = 0;
    operators: str = "{}"
    while i < len(contents):
        if contents[i] == '\n': line += 1;
        if contents[i] == ' ' or contents[i] == '\n' or contents[i] == '\t' or contents[i] == '\r' or contents[i] == '"' or contents[i] == '(' or contents[i] in operators:
            if   buf == "":     pass;
            elif buf == "pop":      ret.append(("pop",  "", line));
            elif buf == "get":      ret.append(("get",  "", line));
            elif buf == "set":      ret.append(("set",  "", line));
            elif buf == "call":     ret.append(("call", "", line));
            elif buf == "putc":     ret.append(("putc", "", line));
            elif buf == "getc":     ret.append(("getc", "", line));
            elif buf == "let":      ret.append(("let",  "", line));
            elif buf == "at":       ret.append(("at",   "", line));
            elif buf == "ifthen":   ret.append(("ifthen", "", line));
            elif buf == "while":    ret.append(("while", "", line));
            else:
                try:
                    ret.append(("integer", str(int(buf,10)), line));
                except ValueError:
                    ret.append(("identifier", buf, line));
            buf = "";
            if contents[i] == '"':
                i+=1;
                while contents[i] != '"':
                    if contents[i] == '\n': line += 1;
                    if i >= len(str):
                        print(f"LEX ERROR: Expected end of string on line {line}");
                        exit(1);
                    buf += contents[i];
                ret.append(("string", buf, line));
                buf = "";
            elif contents[i] == '(':
                i += 1;
                while contents[i] != ')':
                    if contents[i] == '\n': line += 1;
            elif contents[i] in operators:
                ret.append((contents[i], "", line));
            i += 1;
            continue;
        buf += contents[i];
        i += 1;
    return ret;