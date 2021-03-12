import re
from typing import List


Token_Type = int


class Token:
    # enum Token_Type
    CHARACTER = 0
    OPERATOR = 1
    WHITESPACE = 2
    OPENPAREN = 3
    CLOSEPAREN = 4

    def __init__(self, value: str, location: int, ttype: Token_Type):
        self.value = value
        self.location = location
        self.token_type = ttype

    def __repr__(self):
        return str(self.token_type)


regexes = [(re.compile(r'\s+'), Token.WHITESPACE),
           (re.compile(r'(\+|\-|\*\*|\*|\/)'), Token.OPERATOR),
           (re.compile(r'\('), Token.OPENPAREN),
           (re.compile(r'\)'), Token.CLOSEPAREN),
           (re.compile(r'.'), Token.CHARACTER)]


def tokenize(s: str) -> List[Token]:
    tokens = []
    i = 0

    while i < len(s):
        for r, t in regexes:
            m = re.match(r, s[i:])
            if m:
                tokens.append(Token(m.group(0), i, t))
                i += m.end(0)
                break
        else:
            if i < len(s):
                raise Exception(f"Tokenizer failed at {s[i:]}")
            return tokens

    return tokens


if __name__ == "__main__":
    print(tokenize('3+3 *2+sin(2+2* 1+pi)'))
