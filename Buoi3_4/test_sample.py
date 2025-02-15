def add_numbers(a, b):
    return a + b

def test_add_numbers_positive():
    assert add_numbers(2, 3) == 5

def test_add_numbers_negative():
    assert add_numbers(-1, -1) == -2
