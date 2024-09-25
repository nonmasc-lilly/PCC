import typing;

"""ABNF
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
"""

class AST:
    def __init__(self, ttype: str, value: str) -> None:
        self.children = [];
        self.ttype = ttype;
        self.value = value;
    def add_child(self, child) -> None:
        self.children.append(child);
    def __repr__(self, which: int=0) -> str:
        ret: str;
        ret = f"{self.ttype} :: {self.value} :: [";
        if len(self.children) > 0:
            ret += "\n";
            for i in self.children:
                ret += ("\t" * (which+1)) + f"{i.__repr__(which+1)}\n";
            ret += ("\t" * which);
        ret += "]";
        return ret;

def parse_program(lexed: list[tuple[str,str]]) -> AST:
    ret: AST = AST("root","");
    tmp: tuple[int,AST];
    current: int = 0;
    while current < len(lexed):
        tmp = parse_function(lexed, current);
        if tmp[1].ttype == "NULL":
            print(f"PARSER ERROR: unexpected token at {lexed[current][2]} with type {lexed[current][0]}");
            exit(1);
        current += tmp[0];
        ret.add_child(tmp[1]);
    return ret;

def parse_function(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    cur: int = 0;
    ret: AST;
    tmp: AST;
    if lexed[current][0] != "identifier" or lexed[current+1][0] != '{':
        return (0,AST("NULL",""));
    cur = 2;
    ret = AST("function", "");
    ret.add_child(AST("identifier", lexed[current][1]));
    while lexed[current+cur][0] != '}':
        print(f"{lexed[current+cur]} :: {current+cur}");
        tmp = parse_statement(lexed, current+cur);
        if tmp[1].ttype == "NULL":
            print(f"PARSER ERROR: expected token in function at {lexed[current+cur][2]} with type {lexed[current+cur][0]}\n");
            exit(1);
        cur = tmp[0];
        ret.add_child(tmp[1]);
    cur += 1;
    return (cur, ret);
# statement = push / pop / get / set / call / ret / putc / getc / let / if / while
def parse_statement(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    statements: list[typing.Callable[[list[tuple[str,str]], int], tuple[int,AST]]] = [
        parse_push, parse_pop, parse_get, parse_set, parse_call, parse_ret, parse_putc, parse_getc, parse_let, parse_ifthen, parse_while
    ];
    for i in statements:
        tmp: tuple[int,AST] = i(lexed, current);
        if tmp[1].ttype != "NULL": return tmp;
    return (0,AST("NULL",""));

def parse_push(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    if lexed[current][0] != "integer" and lexed[current][0] != "identifier" and lexed[current][0] != "string": return (0,AST("NULL",""));
    return (current+1, AST("push",lexed[current][1]));
def parse_pop(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    if lexed[current][0] != "pop": return (0,AST("NULL",""));
    return (current+1, AST("pop",""));
def parse_get(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    if lexed[current][0] != "get": return (0,AST("NULL",""));
    return (current+1, AST("get",""));
def parse_set(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    if lexed[current][0] != "set": return (0,AST("NULL",""));
    return (current+1, AST("set",""));
def parse_call(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    if lexed[current][0] != "call": return (0,AST("NULL",""));
    return (current+1, AST("call",""));
def parse_ret(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    if lexed[current][0] != "ret": return (0,AST("NULL",""));
    return (current+1, AST("ret",""));
def parse_getc(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    if lexed[current][0] != "getc": return (0,AST("NULL",""));
    return (current+1, AST("getc",""));
def parse_putc(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    if lexed[current][0] != "putc": return (0,AST("NULL",""));
    return (current+1, AST("putc",""));
def parse_let(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    ret: AST;
    if lexed[current][0] != "let": return (0,AST("NULL",""));
    ret = AST("let", "");
    if lexed[current+1][0] != "identifier":
        print(f"PARSER ERROR: expected let identifier at {lexed[current+1][2]}");
        exit(1);
    if lexed[current+2][0] != "at":
        print(f"PARSER ERROR: expected 'at' token at {lexed[current+2][2]}");
        exit(1);
    if lexed[current+3][0] != "integer":
        print(f"PARSER ERROR: expected integer at {lexed[current+3][2]}");
        exit(1);
    ret.add_child(AST("identifier", lexed[current+1][2]));
    ret.add_child(AST("integer", lexed[current+3][2]));
    return (current+4, ret);
def parse_ifthen(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    cur: int;
    ret: AST;
    if lexed[current][0] != "ifthen": return (0,AST("NULL",""));
    if lexed[current+1][0] != "{":
        print(f"PARSER ERROR: expected block after ifthen at {lexed[current+1][2]}");
        exit(1);
    cur = 2;
    ret = AST("ifthen", "");
    while lexed[current+cur][0] != '}':
        tmp = parse_statement(lexed, current+cur);
        if tmp[1].ttype == "NULL":
            print(f"PARSER ERROR: expected token in if statement at {lexed[current+cur][2]} with type {lexed[current+cur][0]}\n");
            exit(1);
        cur += tmp[0];
        ret.add_child(tmp[1]);
    cur += 1;
    return (current+cur, ret);
def parse_while(lexed: list[tuple[str,str]], current: int) -> tuple[int,AST]:
    cur: int;
    if lexed[current][0] != "while": return (0,AST("NULL",""));
    if lexed[current+1][0] != "{":
        print(f"PARSER ERROR: expected block after while at {lexed[current+1][2]}");
        exit(1);
    cur = 2;
    ret = AST("while","");
    while lexed[current+cur][0] != '}':
        tmp = parse_statement(lexed, current+cur);
        if tmp[1].ttype == "NULL":
            print(f"PARSER ERROR: expected token in while loop at {lexed[current+cur][2]} with type {lexed[current+cur][0]}\n");
            exit(1);
        cur += tmp[0];
        ret.add_child(tmp[1]);
    cur += 1;
    return (current+cur, ret);