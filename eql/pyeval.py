from .parser import parse, Node, PrefixNode, BlockNode, TerminalNode
from math import *

# TODO: Move this into another file
def pyeval(s):
    ast_head = parse(s)

    return eval_node(ast_head)

def eval_node(node):
    if isinstance(node, TerminalNode):
        # TODO: replace with something better
        try:
            return int(node.value)
        except ValueError:
            return float(node.value)
    elif isinstance(node, BlockNode):
        return eval_node(node.rhs)
    elif isinstance(node, PrefixNode):
        return eval(f"{node.name}({eval_node(node.rhs)})")
    elif isinstance(node, Node):
        if node.name == "+":
            return eval_node(node.lhs) + eval_node(node.rhs)
        elif node.name == "-":
            return eval_node(node.lhs) - eval_node(node.rhs)
        elif node.name == "*":
            return eval_node(node.lhs) * eval_node(node.rhs)
        elif node.name == "/":
            return eval_node(node.lhs) / eval_node(node.rhs)
        elif node.name == "**":
            return eval_node(node.lhs) ** eval_node(node.rhs)
        elif node.name == ",":
            return f"{eval_node(node.lhs)},{eval_node(node.rhs)}"
    else:
        print(node)
        raise TypeError(f"Type of value passed to eval_node must be a node, not {type(node)}")

