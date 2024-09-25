import sys;
import typing;
import lex;
import parse;

def main(argc: int, argv: list[str]) -> int:
    file: typing.TextIO;
    file_content: str = "";
    lexed: list[tuple[str,str]];
    parsed: AST;
    file = open(argv[1], "r");
    file_content = file.read();
    file.close();
    lexed = lex.lex(file_content);
    print(lexed);
    parsed = parse.parse_program(lexed);
    print(parsed);
    return 0;

if __name__ == "__main__": exit(main(len(sys.argv), sys.argv));