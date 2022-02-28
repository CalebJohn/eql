from .lexer import tokenize
from .queue import Queue, Stack
from .exceptions import MissingOp, MissingLParen, MissingParen, MissingValue, MissingValueAfterSpace


def parse(eq):
    if not eq:
        return []

    tokens = tokenize(eq)
    # Used for syntax checking
    last_t = None
    
    output = Queue()
    operators = Stack()
    for t in tokens:
        # Start with the syntax checks
        if last_t is not None:
            if last_t.isFunc() and not t.isLParen():
                raise(MissingLParen(eq, t))
            if t.isSpace() and last_t.isOp():
                raise(MissingValueAfterSpace(eq, t))
            if t.isOp() and last_t.isOp():
                raise(MissingValue(eq, t))
            if not t.isOp() and last_t.isSpace():
                raise(MissingOp(eq, t))
        else:
            # Special case for when an equation starts with an operator
            if t.isOp():
                raise(MissingValue(eq, t))

        if t.isNumeral():
            output.push(t)
        elif t.isFunc():
            operators.push(t)
        elif t.isSpace():
            while not operators.empty() and not operators.peek().isLParen():
                output.push(operators.pop())
        elif t.isOp():
            p = t.precedence()
            o = operators.peek()
            while (o and o.isOp()
                    and (p < o.precedence()
                        or (p == o.precedence() and t.associativity() == 'l'))):
                output.push(operators.pop())
                o = operators.peek()

            operators.push(t)
        elif t.isLParen():
            operators.push(t)
        elif t.isRParen():
            o = operators.peek()
            while o and not o.isLParen():
                output.push(operators.pop())
                o = operators.peek()
            if not o or not o.isLParen():
                raise(MissingParen(eq, t))
            operators.pop() # discard the left paren
            if not operators.empty() and operators.peek().isFunc():
                output.push(operators.pop())
        # Update last_t for the syntax checker
        last_t = t
    
    while not operators.empty():
        output.push(operators.pop())

    if last_t.isOp():
        raise(MissingValue(eq, last_t))

    return output

