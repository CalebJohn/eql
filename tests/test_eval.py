from eql.eval import evaluate_expression

def test_pyeval_1():
    assert str(evaluate_expression('2+2')) == "4"

def test_pyeval_2():
    assert str(evaluate_expression('tan(2+6*sin58)')) == "-9.65038837702490326364568318240344524383544921875"

def test_pyeval_3():
    assert str(evaluate_expression('tan2+ 6*sin58')) == "3.7721960252457038542672762559959664940834045410156250"

def test_pyeval_4():
    assert str(evaluate_expression('gcd(9,8)* 32')) == "32"

def test_pyeval_6():
    assert str(evaluate_expression('1+2* 6')) == "18"

def test_pyeval_7():
    assert str(evaluate_expression('1+2* 6** 8')) == "5038848"

def test_pyeval_8():
    assert str(evaluate_expression('2+-2')) == "0"

def test_pyeval_9():
    assert str(evaluate_expression('-2+-2')) == "-4"
