from eql.parser import parse

def test_parse_1():
    assert str(parse('2+2')) == '+(2,2)'

def test_parse_2():
    assert str(parse('tan(2+6*sin58)')) == 'tan(+(2,*(6,sin(58))))'

def test_parse_3():
    assert str(parse('tan2+ 6*sin58')) == '+(tan(2),b(*(6,sin(58))))'

def test_parse_3a():
    assert str(parse('tan2 +6*sin58')) == '+(tan(2),*(6,sin(58)))'

def test_parse_4():
    assert str(parse('gcd(9,8)* 32')) == '*(gcd(,(9,8)),b(32))'

def test_parse_5():
    assert str(parse('2**2**3')) == '**(2,**(2,3))'

def test_parse_6():
    assert str(parse('1+2* 6')) == '*(+(1,2),6)'

def test_parse_7():
    assert str(parse('1+2* 6** 8')) == '*(+(1,2),**(6,b(8)))'

def test_parse_7a():
    assert str(parse('1+2* 6** 4+4')) == '*(+(1,2),**(6,b(+(4,4))))'

def test_parse_8():
    assert str(parse('1+2 *6 **8')) == '**(*(+(1,2),6),8)'

def test_parse_9():
    assert str(parse('-2+2')) == '+(-(2),2)'

def test_parse_11():
    assert str(parse('sin0.167')) == 'sin(0.167)'

def test_parse_12():
    assert str(parse('sin(2*pi)')) == 'sin(*(2,pi))'

def test_parse_13():
    assert str(parse('sin(2* 1+pi)')) == 'sin(*(2,b(+(1,pi))))'

def test_parse_14():
    assert str(parse('2* 1+pi* 3/6)')) == '*(2,b(*(+(1,pi),/(3,6))))'
