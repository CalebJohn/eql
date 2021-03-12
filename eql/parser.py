from typing import Any, List, Optional, Tuple
from .lexer import Token, tokenize


Ast = List[Token]


class EQLError(Exception):
    """A syntax error with the EQL match language"""
    def __init__(self, token: Token, message: str):
        self.tok = token
        self.location = token.location
        self.message = message
        super().__init__(message)

    def print(self):
        print("^".rjust(self.location + 1))
        print(self.message.rjust(len(self.message) // 2 + self.location))


def trailingop(ex: List[Any]) -> Tuple[Ast, Optional[Token]]:
    if not ex or not isinstance(ex[-1], Token):
        return [], None

    if ex[-1].token_type == Token.OPERATOR:
        return ex[:-1], ex[-1]

    return ex, None


def leadingop(ex: List[Any]) -> Tuple[Optional[Token], Ast]:
    if not ex or not isinstance(ex[0], Token):
        return None, []

    if ex[0].token_type == Token.OPERATOR:
        return ex[0], ex[1:]

    return None, ex


def ast_to_str(ast: Ast) -> str:
    s = ""
    for c in ast:
        s += c.value

    return s


def split_ast(ast: Ast) -> List[Ast]:
    l: List[Ast] = []
    l.append([])
    for c in ast:
        if c.token_type == Token.WHITESPACE:
            l.append([])
        else:
            l[-1].append(c)

    return l


# The parser will simply output a string that can be
# processed by either python or sympy
# This function is simply a wrapper around parse_with_error that
# adds some pretty error reporting
def parse(s: str, allow_partial: bool = False) -> str:
    try:
        return ast_to_str(parse_parens(tokenize(s), allow_partial))
    except EQLError as e:
        print(s)
        e.print()
        raise e


def parse_parens(eq: list, allow_partial: bool) -> Ast:
    """The first step is to split the parsing up based on parenthesis"""
    expr: Ast = []
    while len(eq):
        c = eq.pop(0)
        if c.token_type == Token.OPENPAREN:
            expr += parse_parens(eq, allow_partial)
        elif c.token_type == Token.CLOSEPAREN:
            break
        else:
            expr += [c]

    return parse_without_parens(expr, allow_partial)


def flatten(parsed_tree: List[Any]) -> Ast:
    f = []
    for t in parsed_tree:
        if t and isinstance(t, list):
            f += [Token("(", -1, Token.OPENPAREN)] + flatten(t) + [Token(")", -1, Token.CLOSEPAREN)]
        elif t:
            f += [t]

    return f


def parse_without_parens(s: Ast, allow_partial: bool) -> Ast:
    # Calling this an ast is fairly tongue in cheek
    groups = split_ast(s)

    if not groups:
        return []

    leading, _ = leadingop(groups[0])
    if leading and leading.value != "-":
        raise EQLError(groups[0][0], "An EQL expression cannot start with an operator")

    if not allow_partial and trailingop(groups[-1])[1]:
        raise EQLError(groups[-1][-1], "An EQL expression cannot end with an operator")

    # result will ultimately contains Asts, but they're nested
    result: List[Any] = []
    for ex in groups:
        if not ex:
            continue
        body, trailing = trailingop(ex)
        leading, body = leadingop(body)
        if leading:
            if result and trailingop(result)[1] and leading.value != "-":
                raise EQLError(leading, "Extra operator")

            if trailing:
                result = [result + [leading] + body, trailing]
            else:
                result = [result + [leading] + body]
        elif trailing:
            result = [result + body, trailing]
        else:
            if result and not trailingop(result)[1]:
                raise EQLError(ex[0], "Missing operator")

            result = [result + ex]

    return flatten(result)


if __name__ == "__main__":
    print(parse("1+2* 6"))
    parse('1+1+1+1+1+1+1+1+1+1+1+1+ +1')
    print(parse("1+2 *6"))
    print(parse('2+2 +4* 3'))
    print(parse('2+2'))
    # print(parse('tan(2+6*sin(58))'))
    # print(parse('gcd(9,8)* 32'))
    # print(parse('2**2**3'))
    # print(parse('1+2* 6'))
    # print(parse('1+2* 6** 8'))
    # print(parse('1+2* 6** 4+4'))
    # print(parse('2+2 *3 +4'))
    # print(parse('2+2* 3+4'))
    # print(parse('2+2 *3*3'))
    # print(parse('2+2* 3*3'))
    # print(parse('2+2 +4 *3'))
    # print(parse('1+2 *6 **8'))
    # print(parse('-2+2'))
    # print(parse('sin(2*pi)'))
    # print(parse('3+3 *2+sin(2+2* 1+pi)'))
    # print(parse('2* 1+pi* 3/6'))
    # print(parse('2* 1+pi* (3/6)'))
    # print(parse('2/600e-9'))
    # print(parse('3.2*6.5+8.0 *6'))
