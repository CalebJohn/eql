from .queue import Stack

import decimal
import fractions
from math import pi, tau, e
import numbers

"""
This module implements a generic way to use pythons number libraries to 
represent numbers in eql calculations.

The default is to represent numbers as fractions internally and convert
to the correct representation at display time. The fractions library 
represents numbers as an exact fraction and can handle operations at speed
this is ideal for use as a calculator.

The decimal library can also be used. It is useful when tracking
significant digits. e.g. 0.40 * 0.25 == 0.20
"""

allowed_functions = ['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 'copysign',
                     'cos', 'cosh', 'degrees', 'erf', 'erfc', 'exp', 'expm1', 'fabs', 'factorial', 'floor',
                     'fmod', 'frexp', 'fsum', 'gamma', 'gcd', 'hypot', 'inf', 'isclose', 'isfinite', 'isinf',
                     'isnan', 'ldexp', 'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'nan', 'pow',
                     'radians', 'remainder', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'trunc']

math = __import__('math', fromlist=allowed_functions)


def evaluate(rpn: list, ntype: numbers.Number = fractions.Fraction) -> numbers.Number:
    if not rpn:
        return None

    # prec is set to enable
    # (Decimal('100e30') + Decimal('6.626E-34')**2) - Decimal('100e30')
    # == Decimal('4.3903876E-67')
    # I don't know why I chose this example, but I did
    # Increasing precision comes at a run time cost, and this is the point of tradeoff that I chose
    ctx = decimal.Context(prec=110)
    decimal.setcontext(ctx)

    stack = Stack()
    for t in rpn:
        if t.isNumeral():
            if t.isComplex():
                stack.push(complex(str(t)))
            else:
                stack.push(ntype(str(t)))
        elif t.isFunc():
            if t.value in allowed_functions:
                arg = stack.pop()
                if type(arg) != tuple:
                    arg = [arg]
                # special case because for functions that only accept ints
                if t.value in ['gcd']:
                    try:
                        arg = [int(a) for a in arg]
                    except ValueError:
                        raise ValueError('gcd can only operate on integers')
                func = getattr(math, t.value)
                # The result of math is a float, so we need to convert
                # it back to a decimal
                stack.push(ntype(func(*arg)))
            else:
                raise ValueError(f"{t.value} is unsupported by eql")
        elif t.isOp():
            r = stack.pop()
            l = stack.pop()
            if t.value == ',':
                stack.push((l, r))
            else:
                args = list(l) if type(l) == tuple else [l]
                args.extend(r if type(r) == tuple else [r])
                stack.push(t.as_func()(*args))

    return stack.pop()
