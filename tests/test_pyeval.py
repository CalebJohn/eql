from eql.pyeval import pyeval

def test_pyeval_1():
    assert str(pyeval('2+2')) == "4"

def test_pyeval_2():
    assert str(pyeval('tan(2+6*sin58)')) == "-9.650388377024903"

def test_pyeval_3():
    assert str(pyeval('tan2+ 6*sin58')) == "3.7721960252457034"

def test_pyeval_4():
    assert str(pyeval('gcd(9,8)* 32')) == "32"

def test_pyeval_6():
    assert str(pyeval('1+2* 6')) == "18"

def test_pyeval_7():
    assert str(pyeval('1+2* 6** 8')) == "5038848"

def test_pyeval_8():
    assert str(pyeval('2+-2')) == "0"

def test_pyeval_9():
    assert str(pyeval('-2+-2')) == "-4"
