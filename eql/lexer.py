import re
from typing import List
import operator


Token_Type = int

precedence = {
        ',': 0,
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '**': 3,
}
associativity = {
        ',': 'l',
        '+': 'l',
        '-': 'l',
        '*': 'l',
        '/': 'l',
        '**': 'r',
}
operator_map = {
        '*': operator.mul,
        '/': operator.truediv,
        '+': operator.add,
        '-': operator.sub,
        '**': operator.pow,
        }


class NotOperator(Exception):
    pass

class Token:
    # enum Token_Type
    CHARACTER = 0
    OPERATOR = 1
    OPENPAREN = 2
    CLOSEPAREN = 3
    WHITESPACE = 4
    FUNCTION = 5

    def __init__(self, value: str, location: int, ttype: Token_Type):
        self.value = value
        self.location = location
        self.token_type = ttype

    def __repr__(self):
        return str(self.value)

    def isNumeral(self):
        return self.token_type == self.CHARACTER
    def isOp(self):
        return self.token_type == self.OPERATOR
    def isFunc(self):
        return self.token_type == self.FUNCTION
    def isLParen(self):
        return self.token_type == self.OPENPAREN
    def isRParen(self):
        return self.token_type == self.CLOSEPAREN
    def isSpace(self):
        return self.token_type == self.WHITESPACE
    def isComplex(self):
        return self.value[-1].lower() == 'j'

    def precedence(self):
        if not self.isOp():
            raise(NotOperator(f"Token {self.value} does not have a precedence ch:{self.location}"))

        return precedence[self.value]

    def associativity(self):
        if not self.isOp():
            raise(NotOperator(f"Token {self.value} does not have an associativity ch:{self.location}"))
        return associativity[self.value]

    def as_func(self):
        if not self.isOp():
            raise(NotOperator(f"Token {self.value} does not represent a function ch:{self.location}"))
        return operator_map[self.value]



regexes = [(re.compile(r'\s+'), Token.WHITESPACE),
           (re.compile(r'(\+|\-|\*\*|\*|\/|,)'), Token.OPERATOR),
           (re.compile(r'\('), Token.OPENPAREN),
           (re.compile(r'\)'), Token.CLOSEPAREN),
           (re.compile(r'-?\d+\.?\d*(?:[eE][-+]?\d+)?j?|pi|e|tau'), Token.CHARACTER),
           (re.compile(r'[a-zA-z]+'), Token.FUNCTION)]


def tokenize(s: str) -> List[Token]:
    tokens = []
    i = 0

    while i < len(s):
        for r, t in regexes:
            m = re.match(r, s[i:])
            if m:
                if t == Token.OPERATOR and m.group(0) == '-':
                    if len(tokens) == 0 or tokens[-1].isOp() or tokens[-1].isLParen():
                        continue
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
