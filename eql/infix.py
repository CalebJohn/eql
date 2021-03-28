from .queue import Stack

# Convert the rpn token list into an "infix" string
def to_infix(rpn):
    if not rpn:
        return ''

    stack = Stack()
    for t in rpn:
        if t.isNumeral():
            stack.push(t)
        elif t.isFunc():
            stack.push(f"{t.value}({stack.pop()})")
        elif t.isOp():
            r = stack.pop()
            l = stack.pop()
            if t.value == ',':
                stack.push(f"{l}{t.value}{r}")
            else:
                stack.push(f"({l}{t.value}{r})")

    return stack.pop()
