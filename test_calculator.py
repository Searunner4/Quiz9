import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 5) == 4
    assert add(0, 0) == 0
    assert add(-3,-7) == -10
    assert add(2.5, 3.5) == 6.0
    assert add(-7, 4) == -3

def test_subtract():
    assert subtract(10, 4) == 6
    assert subtract(-2, 3) == -5
    assert subtract(0,5) == -5
    assert subtract(7.5, 2.5) == 5.0
    assert subtract(-10, 5) == -15
    assert subtract(-12, 50) == 38

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 6) == -12
    assert multiply(0, 100) == 0
    assert multiply(-3, -3) == 9
    assert multiply(2.5, 4) == 10.0

def test_divide():
    assert divide(-9, 3) == -3
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5
    assert divide(-8,-2) == 4
    try:
        divide(5,0)
    except ValueError as e:
        assert str(e) == "Cannot divide by zero!"