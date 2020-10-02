from .parser import parse, Node, PrefixNode, BlockNode, TerminalNode
import decimal
from math import *

def evaluate_expression(s):
    ast_head = parse(s)

    return eval_node(ast_head)

def eval_node(node):
    # prec is set to enable
    # (Decimal('100e30') + Decimal('6.626E-34')**2) - Decimal('100e30')
    # == Decimal('4.3903876E-67')
    ctx = decimal.Context(prec=110)
    decimal.setcontext(ctx)

    if isinstance(node, TerminalNode):
            return decimal.Decimal(node.value)
    elif isinstance(node, BlockNode):
        return eval_node(node.rhs)
    elif isinstance(node, PrefixNode):
        return decimal.Decimal(eval(f"{node.name}({eval_node(node.rhs)})"))
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

