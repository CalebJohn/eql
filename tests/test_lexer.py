from eql.parser import Lexer, EOEToken


def join_lexer(s):
    l = Lexer(s)
    r = []
    t = next(l)
    while not isinstance(t, EOEToken):
        r.append(str(t)) 
        t = next(l)
    return ''.join(r)

def test_lexer_1():
    assert join_lexer('2+2') == '2+2'

def test_lexer_2():
    assert join_lexer('tan(2+6*sin58)') == 'tan(2+6*sin58)'

def test_lexer_3():
    assert join_lexer('tan2+ 6*sin58') == 'tan2+ 6*sin58'

def test_lexer_3a():
    assert join_lexer('tan2 +6*sin58') == 'tan2 +6*sin58'

def test_lexer_4():
    assert join_lexer('gcd(9,8)* 32') == 'gcd(9,8)* 32'

def test_lexer_5():
    assert join_lexer('2**2**3') == '2**2**3'

def test_lexer_6():
    assert join_lexer('1+2* 6') == '1+2* 6'

def test_lexer_7():
    assert join_lexer('1+2* 6** 8') == '1+2* 6** 8'

def test_lexer_7a():
    assert join_lexer('1+2* 6** 4+4') == '1+2* 6** 4+4'

def test_lexer_8():
    assert join_lexer('1+2 *6 **8') == '1+2 *6 **8'

def test_lexer_9():
    assert join_lexer('-2+2') == '-2+2'

def test_lexer_11():
    assert join_lexer('sin0.167') == 'sin0.167'

def test_lexer_12():
    assert join_lexer('sin(2*pi)') == 'sin(2*pi)'

def test_lexer_13():
    assert join_lexer('sin(2* 1+pi)') == 'sin(2* 1+pi)'

def test_lexer_14():
    assert join_lexer('2* 1+pi* 3/6') == '2* 1+pi* 3/6'
