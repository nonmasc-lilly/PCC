import parse;
import typing;

class STATE:
    def __init__(self):
        self.ret: bytes = b'';
        self.current_location: int = 0;
        self.function_symbols:   list[tuple[str,int]] = [];
        self.scoped_let_symbols: list[list[tuple[str,int]]] = [];
    def add_func(self, name: str):
        self.function_symbols.append((name, current_location));
    def new_scope(self) -> int:
        self.scoped_let_symbols.append([]);
        return len(self.scoped_let_symbols);

def compile_program(ast: parse.AST):
    state: STATE = STATE();
    for i in ast: compile_function(ast, state);
    return state.ret;

def compile_function(ast: parse.AST, state: STATE):
    scope: int;
    state.add_func(ast.children[0].value);
    scope = state.new_scope();
    for i in ast.children[1:]:
        compile_statement(ast, state, scope);

def compile_statement(ast: parse.AST, state: STATE, scope: int):
    statements: list[typing.Callable[[parse.AST, STATE, int], None]] = [
        compile_push, compile_pop, compile_get, compile_set, compile_call, compile_ret, compile_putc, compile_getc, compile_let, compile_ifthen, compile_while
    ];
    for i in statements:
        i(ast, state, scope);

def compile_push(ast: parse.AST, state: STATE, scope: int):
    if ast.ttype != "push": return;
    try:
        x = int(ast.value,10);
        state.add_code(b'\x00'+x.to_bytes);
    except ValueError:
        