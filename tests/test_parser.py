from eql.parser import EQLError, parse
import pytest


def test_parse():
    assert parse('2+2') == '(2+2)'
    assert parse("1+2* 6") == '((1+2)*6)'
    assert parse("1+2 *6") == '((1+2)*6)'
    assert parse('2+2 +4* 3') == '(((2+2)+4)*3)'
    assert parse('2+2') == '(2+2)'
    assert parse('tan(2+6*sin(58))') == '(tan(2+6*sin(58)))'
    assert parse('gcd(9,8)* 32') == '((gcd(9,8))*32)'
    assert parse('2**2**3') == '(2**2**3)'
    assert parse('1+2* 6') == '((1+2)*6)'
    assert parse('1+2* 6** 8') == '(((1+2)*6)**8)'
    assert parse('1+2* 6** 4+4') == '(((1+2)*6)**4+4)'
    assert parse('2+2 *3 +4') == '(((2+2)*3)+4)'
    assert parse('2+2* 3+4') == '((2+2)*3+4)'
    assert parse('2+2 *3*3') == '((2+2)*3*3)'
    assert parse('2+2* 3*3') == '((2+2)*3*3)'
    assert parse('2+2 +4 *3') == '(((2+2)+4)*3)'
    assert parse('1+2 *6 **8') == '(((1+2)*6)**8)'
    assert parse('-2+2') == '(-2+2)'
    assert parse('sin(2*pi)') == '(sin(2*pi))'
    assert parse('3+3 *2+sin(2+2* 1+pi)') == '((3+3)*2+sin((2+2)*1+pi))'
    assert parse('2* 1+pi* 3/6') == '(((2)*1+pi)*3/6)'
    assert parse('2* 1+pi* (3/6)') == '(((2)*1+pi)*(3/6))'
    assert parse('2/600e-9') == '(2/600e-9)'
    assert parse('3.2*6.5+8.0 *6') == '((3.2*6.5+8.0)*6)'


def test_parse_exceptions():
    with pytest.raises(EQLError) as e:
        assert parse('1 1')

    with pytest.raises(EQLError) as e:
        assert parse('1* *1')

    with pytest.raises(EQLError) as e:
        assert parse('*1 *1')

    with pytest.raises(EQLError) as e:
        assert parse('1 *1*')
