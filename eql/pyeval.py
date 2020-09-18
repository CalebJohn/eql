from .parser import parse, Node, PrefixNode, BlockNode, TerminalNode
from expect import expect
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


if __name__ == "__main__":
    @expect("4")
    def pyeval_test_1():
        return pyeval('2+2')

    @expect("-9.650388377024903")
    def pyeval_test_2():
        return pyeval('tan(2+6*sin58)')

    @expect("3.7721960252457034")
    def pyeval_test_3():
        return pyeval('tan2+ 6*sin58')

    @expect("32")
    def pyeval_test_4():
        return pyeval('gcd(9,8)* 32')

    @expect("18")
    def pyeval_test_6():
        return pyeval('1+2* 6')

    @expect("5038848")
    def pyeval_test_7():
        return pyeval('1+2* 6** 8')

    @expect("0")
    def pyeval_test_8():
        return pyeval('2+-2')

    @expect("-4")
    def pyeval_test_9():
        return pyeval('-2+-2')
