import re

binary_re = re.compile('(\+|\-|\*\*|\*|\/|,|\s)')
functionre = re.compile("([a-z|A-Z]+)((?:[0-9]+\.)?[0-9]*)")
number_re = re.compile('(?:((?:[0-9]*\.)?[0-9]+)(?:E((?:[0-9]+\.)?[0-9]+))?(?:pi|e|tau)?|pi|e|tau)')

# Parent type for all tokens
class PrattToken:
    lbp = 0
    def __init__(self, lex, value, start, end):
        self.lexer = lex
        self.value = value
        self.start = start
        self.end = end
    def __repr__(self):
        return f"{self.value}"
    def parse(self, token, rbp=0):
        return parse_expression(self.lexer, rbp, token)
    def nud(self, token=None):
        raise SyntaxError(f"Nud not implemented for {type(self).__name__}")
    def led(self, left, token):
        right = self.parse(token, self.lbp)
        return InfixNode(self.value, left, right)

class SpaceToken(PrattToken):
    r = '\s+'
    lbp = 5
    def nud(self, token):
        return BlockNode(self.parse(token))

    def led(self, left, token):
        if not isinstance(token, (MulToken, DivToken, PlusToken, MinusToken, ExpToken, ArgToken)):
            raise SyntaxError(f"Need an operator for space chaining got {token} at {self.end}")

        t = next(self.lexer)
        return token.led(left, t)

class ArgToken(PrattToken):
    r = '\,'
    lbp = 20
class ExpToken(PrattToken):
    r = '\*\*'
    lbp = 50
    def led(self, left, token):
        right = self.parse(token, self.lbp - 1)
        return InfixNode(self.value, left, right)

class MulToken(PrattToken):
    r = '\*'
    lbp = 40
class DivToken(PrattToken):
    r = '\/'
    lbp = 40
class PlusToken(PrattToken):
    r = '\+'
    lbp = 30
class MinusToken(PlusToken):
    r = '\-'
    lbp = 30
    def nud(self, token):
        return PrefixNode(self.value, self.parse(token, 100))
class FuncArgToken(PrattToken):
    r = '([a-z|A-Z]+)((?:[0-9]+\.)?[0-9]+)'
    lbp = 10
    def nud(self, token):
        m = re.match(self.r, self.value)
        return PrefixNode(m.group(1), TerminalNode(m.group(2)))
class FuncToken(PrattToken):
    r = '([a-z|A-Z]+)'
    lbp = 90
    def nud(self, token):
        if not isinstance(token, LeftParenToken):
            raise SyntaxError(f"Function calls of multiple values require parentheses! {self.value} missing opening paren at {self.start}")

        # right = token.nud(next(self.lexer))
        right = self.parse(token, self.lbp)

        return PrefixNode(self.value, right)
class NumberToken(PrattToken):
    r = number_re
    def nud(self, token):
        return TerminalNode(self.value)
class LeftParenToken(PrattToken):
    r = '\('
    def nud(self, token):
        right = self.parse(token)

        if not isinstance(self.lexer.current(), RightParenToken):
            raise SyntaxError(f"( Must eventually be followed by a ), expected ) but got {token}")

        next(self.lexer)
        return right
class RightParenToken(PrattToken):
    r = '\)'
    def nud(self, token):
        return TerminalNode("Close")
class EOEToken(PrattToken):
    def __init__(self, expr):
        super().__init__(None, "EOE", len(expr), len(expr))


class Lexer:
    def __init__(self, expr):
        self.expr = expr
        self.index = 0
        self.previous_token = None

    # Move forward the length of the match
    def eat(self, token):
        self.index = token.end

    # un-eat the previous_token
    def backup(self):
        self.index = self.previous_token.start

    def __next__(self):
        token = self.parse_token(self.expr, self.index)
        if not isinstance(token, EOEToken):
            self.eat(token)
        # print("Next ate:", token)

        self.previous_token = token

        return token

    def current(self):
        return self.previous_token

    def parse_token(self, expr, index):
        start = index
        if start == len(expr):
            return EOEToken(expr)
    
        # CAUTION, the index of these res correspond to the enum above
        res = [SpaceToken, ArgToken, ExpToken, MulToken, DivToken, PlusToken, MinusToken, NumberToken,FuncArgToken, FuncToken,  LeftParenToken, RightParenToken]
    
        for t in res:
            match = re.match(t.r, expr[index:])
            if match:
                end = start + match.span()[1]
                value = match.group(0)
                return t(self, value, start, end)
        else:
            raise SyntaxError(f'Unexpected token {expr[index:]} at {index}')


# Infix node is a special helper that will enable us to apply 
# block level nodes
def InfixNode(name, lhs, rhs):
    node = Node(name, lhs, rhs)
    if isinstance(rhs, Node) and rhs.rhs_block:
        node.rhs = rhs.lhs
        node.parent = rhs
        node.parent.lhs = node
        node.parent.rhs = rhs.rhs.rhs
        return node.parent

    return node

class Node:
    def __init__(self, name, lhs, rhs):
        self.name = name
        self.lhs = lhs
        self.rhs = rhs
        lhs.parent = self
        rhs.parent = self
        self.parent = None
        self.rhs_block = isinstance(rhs, BlockNode)

    def __repr__(self):
        return f"{self.name}({self.lhs},{self.rhs})"

class PrefixNode(Node):
    parent = None
    def __init__(self, name, rhs):
        super().__init__(name, TerminalNode(None), rhs)

    def __repr__(self):
        return f"{self.name}({self.rhs})"

# Temporary node to support block functions
class BlockNode:
    def __init__(self, rhs):
        self.rhs = rhs
    def __repr__(self):
        return f"b({self.rhs})"

class TerminalNode:
    parent = None
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)

    def isempty(self):
        return self.value is None


def parse(s):
    lexer = Lexer(s)

    token = next(lexer)

    ast = token.parse(token)

    if not isinstance(next(lexer), EOEToken):
        raise SyntaxError(f"Expected an end of expression but got {lexer.previous_token}")

    return ast

def parse_expression(lexer, rbp=0, t=None):
    token = next(lexer)
    # print(t, token)
    left = t.nud(token)
    # After recursive calls we want to catch up to the current token
    token = lexer.current()
    while rbp < token.lbp:
        t = token
        token = next(lexer)
        left = t.led(left, token)
        # After recursive calls we want to catch up to the current token
        token = lexer.current()
    return left


