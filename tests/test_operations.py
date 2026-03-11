import pytest
from app.operations import (
    Operation, Add, Subtract, Multiply, Divide, Power, Root, Modulus, IntegerDivision, Percentage, AbsoluteDifference, OperationFactory
)
from app.exceptions import InvalidOperationError

@pytest.mark.parametrize(
    "cls, a, b, expected",
    [
        (Add, 2, 3, 5),
        (Subtract, 5, 3, 2),
        (Multiply, 2, 3, 6),
        (Divide, 6, 3, 2),
        (Power, 2, 3, 8),
        (Root, 9, 2, 3.0),
        (Modulus, 10, 3, 1),
        (IntegerDivision, 10, 3, 3),
        (Percentage, 50, 200, 25.0),
        (AbsoluteDifference, 5, 3, 2),
        (AbsoluteDifference, 3, 5, 2)
    ]
)
def test_operations_execute(cls, a, b, expected):
    assert cls().execute(a, b) == expected

def test_divide_by_zero_message():
    with pytest.raises(ZeroDivisionError, match="cannot divide by zero"):
        Divide().execute(10, 0)

def test_modulus_by_zero_message():
    with pytest.raises(ZeroDivisionError, match="cannot take modulus by zero"):
        Modulus().execute(10, 0)

def test_integer_division_by_zero_message():
    with pytest.raises(ZeroDivisionError, match="cannot take integer division by zero"):
        IntegerDivision().execute(10, 0)

def test_percentage_zero_denominator_message():
    """Percentage operation should raise ZeroDivisionError with informative message for zero denominator."""
    percentage = Percentage()
    with pytest.raises(ZeroDivisionError, match="cannot calculate percentage with zero as denominator"):
        percentage.execute(50, 0)

def test_root_zeroth_root():
    with pytest.raises(ZeroDivisionError, match="zeroth root"):
        Root().execute(9, 0)

def test_root_even_negative():
    with pytest.raises(ValueError, match="even root"):
        Root().execute(-9, 2)

@pytest.mark.parametrize(
    "token, expected_cls",
    [
        ("+", Add),
        ("add", Add),
        ("-", Subtract),
        ("subtract", Subtract),
        ("*", Multiply),
        ("mul", Multiply),
        ("/", Divide),
        ("div", Divide),
        ("^", Power),
        ("**", Power),
        ("pow", Power),
        ("root", Root),
        ("rt", Root),
        ("mod", Modulus),
        ("%", Modulus),
        ("intdiv", IntegerDivision),
        ("//", IntegerDivision),
        ("percentage", Percentage),
        ("absdiff", AbsoluteDifference)
    ],
)
def test_factory_create(token, expected_cls):
    op = OperationFactory.create(token)
    assert isinstance(op, expected_cls)

@pytest.mark.parametrize("bad", ["", " ", "sqrt"])
def test_factory_invalid(bad):
    with pytest.raises(InvalidOperationError, match="Invalid operation"):
        OperationFactory.create(bad)

def test_absolute_difference_with_negatives():
    """Test absolute difference handles negative numbers correctly."""
    assert AbsoluteDifference().execute(-10, -5) == 5
    assert AbsoluteDifference().execute(-5, -10) == 5

def test_percentage_edge_cases():
    assert Percentage().execute(0, 100) == 0.0
    assert Percentage().execute(100, 100) == 100.0

def test_integer_division_returns_int():
    """Verify integer division returns integer type."""
    result = IntegerDivision().execute(10, 3)
    assert result == 3
    assert isinstance(result, int)

def test_modulus_with_floats():
    """Test modulus works with float inputs."""
    result = Modulus().execute(10.5, 3.0)
    assert result == pytest.approx(1.5, rel=1e-9)

def test_operation_is_abstract():
    from abc import ABC
    assert issubclass(Operation, ABC)
    with pytest.raises(TypeError):
        Operation()  # can't instantiate