# test_calculator.py

import pytest
from calculator import Calculator

@pytest.fixture
def calc():
    """A pytest fixture to instantiate the Calculator class before each test."""
    return Calculator()

@pytest.mark.parametrize(
    "a, b, expected", 
    [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 5, 4),
        (10, -5, 5),
    ]
)
def test_add(calc, a, b, expected):
    """Test the add function with multiple sets of inputs."""
    assert calc.add(a, b) == expected

@pytest.mark.parametrize(
    "a, b, expected", 
    [
        (5, 2, 3),
        (0, 0, 0),
        (3, 5, -2),
        (-5, -5, 0),
    ]
)
def test_subtract(calc, a, b, expected):
    """Test the subtract function with multiple sets of inputs."""
    assert calc.subtract(a, b) == expected

@pytest.mark.parametrize(
    "a, b, expected", 
    [
        (2, 3, 6),
        (0, 5, 0),
        (-1, 4, -4),
        (-3, -3, 9),
    ]
)
def test_multiply(calc, a, b, expected):
    """Test the multiply function with multiple sets of inputs."""
    assert calc.multiply(a, b) == expected

def test_divide(calc):
    """Test the divide function for a valid scenario."""
    result = calc.divide(10, 2)
    assert result == 5

def test_divide_by_zero_raises_error(calc):
    """Test that dividing by zero raises the correct exception."""
    with pytest.raises(ValueError) as exc:
        calc.divide(10, 0)
    assert "Cannot divide by zero" in str(exc.value)
