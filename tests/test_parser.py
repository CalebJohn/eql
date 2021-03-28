from eql.parser import parse
from eql.exceptions import MissingOp, MissingValue, MissingParen, MissingValueAfterSpace
import pytest


def test_parse():
    assert repr(parse('2+2')) == '[2, 2, +]'
    assert repr(parse("1+2 *6")) == '[1, 2, +, 6, *]'
    assert repr(parse('2+2 +4 *3')) == '[2, 2, +, 4, +, 3, *]'
    assert repr(parse('tan(2+6*sin(58))')) == '[2, 6, 58, sin, *, +, tan]'
    assert repr(parse('gcd(9,8) *32')) == '[9, 8, ,, gcd, 32, *]'
    assert repr(parse('2**2**3')) == '[2, 2, 3, **, **]'
    assert repr(parse('1+2 *6')) == '[1, 2, +, 6, *]'
    assert repr(parse('1+2 *6 **8')) == '[1, 2, +, 6, *, 8, **]'
    assert repr(parse('1+2 *6 **4+4')) == '[1, 2, +, 6, *, 4, **, 4, +]'
    assert repr(parse('2+2 *3 +4')) == '[2, 2, +, 3, *, 4, +]'
    assert repr(parse('2+2 *3+4')) == '[2, 2, +, 3, *, 4, +]'
    assert repr(parse('2+2 *3*3')) == '[2, 2, +, 3, 3, *, *]'
    assert repr(parse('2+2 +4 *3')) == '[2, 2, +, 4, +, 3, *]'
    assert repr(parse('-2+2')) == '[-2, 2, +]'
    assert repr(parse('2+-1')) == '[2, -1, +]'
    assert repr(parse('2-1')) == '[2, 1, -]'
    assert repr(parse('sin(2*pi)')) == '[2, pi, *, sin]'
    assert repr(parse('3+3 *2+sin(2+2 *1+pi)')) == '[3, 3, +, 2, *, 2, 2, +, 1, *, pi, +, sin, +]'
    assert repr(parse('2 *1+pi *3/6')) == '[2, 1, *, pi, +, 3, 6, /, *]'
    assert repr(parse('2 *1+pi *(3/6)')) == '[2, 1, *, pi, +, 3, 6, /, *]'
    assert repr(parse('2/600e-9')) == '[2, 600e-9, /]'
    assert repr(parse('3.2*6.5+8.0 *6')) == '[3.2, 6.5, *, 8.0, +, 6, *]'


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
