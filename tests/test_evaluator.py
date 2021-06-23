from eql.parser import parse
from eql.evaluator import evaluate
import pytest

cases = {
    '2+2':         '4',
    '0.1+0.2':     '3/10',
    '97/99':       '97/99',
    'gcd(51,17)':  '17',
    '1+1j':        '(1+1j)',
    '1/3 *(1+1j)': '(0.3333333333333333+0.3333333333333333j)',
    '1/3 *(1/3)':  '1/9',
    '2**2**3':     '256',
    '(100e69+1) -100e69': '1',
    '100e30+6.626e-34**2 -100e30': '10975969/25000000000000000000000000000000000000000000000000000000000000000000000000',
}


@pytest.mark.parametrize("equation,result", cases.items())
def test_parse(equation, result):
    assert str(evaluate(parse(equation))) == result
