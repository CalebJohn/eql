from eql.parser import parse
from eql.exceptions import MissingOp, MissingValue, MissingParen, MissingValueAfterSpace
import pytest

cases = {
    '2+2': '[2, 2, +]',
    "1+2 *6": '[1, 2, +, 6, *]',
    '2+2 +4 *3': '[2, 2, +, 4, +, 3, *]',
    'tan(2+6*sin(58))': '[2, 6, 58, sin, *, +, tan]',
    'gcd(9,8) *32': '[9, 8, ,, gcd, 32, *]',
    '2**2**3': '[2, 2, 3, **, **]',
    '1+2 *6': '[1, 2, +, 6, *]',
    '1+2 *6 **8': '[1, 2, +, 6, *, 8, **]',
    '1+2 *6 **4+4': '[1, 2, +, 6, *, 4, **, 4, +]',
    '2+2 *3 +4': '[2, 2, +, 3, *, 4, +]',
    '2+2 *3+4': '[2, 2, +, 3, *, 4, +]',
    '2+2 *3*3': '[2, 2, +, 3, *, 3, *]',
    '2+2 +4 *3': '[2, 2, +, 4, +, 3, *]',
    '-2+2': '[-2, 2, +]',
    '2+-1': '[2, -1, +]',
    '2-1': '[2, 1, -]',
    'sin(2*pi)': '[2, pi, *, sin]',
    '3+3 *2+sin(2+2 *1+pi)': '[3, 3, +, 2, *, 2, 2, +, 1, *, pi, +, sin, +]',
    '2 *1+pi *3/6': '[2, 1, *, pi, +, 3, *, 6, /]',
    '2 *1+pi *(3/6)': '[2, 1, *, pi, +, 3, 6, /, *]',
    '2/600e-9': '[2, 600e-9, /]',
    '3.2*6.5+8.0 *6': '[3.2, 6.5, *, 8.0, +, 6, *]',
    '0.5/100*4625': '[0.5, 100, /, 4625, *]',
}


@pytest.mark.parametrize("equation,rpn", cases.items())
def test_parse(equation, rpn):
    assert repr(parse(equation)) == rpn


def test_parse_exceptions():
    with pytest.raises(MissingOp) as e:
        assert parse('1 1')


    with pytest.raises(MissingParen) as e:
        assert parse('1*1)')

    with pytest.raises(MissingValueAfterSpace) as e:
        assert parse('1* *1')

    with pytest.raises(MissingValue) as e:
        assert parse('*1 *1')

    with pytest.raises(MissingValue) as e:
        assert parse('1 *1*')
