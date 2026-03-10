import pytest
from datetime import datetime
from pathlib import Path
from app.calculator import Calculator, LoggingObserver, AutoSaveObserver
from app.history import History
from app.exceptions import InvalidOperationError


@pytest.mark.parametrize(
    "a, op, b, expected",
    [
        (5, "+", 3, 8),
        (5, "add", 3, 8),
        (10, "-", 3, 7),
        (10, "subtract", 3, 7),
        (4, "*", 5, 20),
        (4, "mul", 5, 20),
        (20, "/", 4, 5),
        (20, "div", 4, 5),
        (2, "^", 3, 8),
        (2, "pow", 3, 8),
        (8, "root", 3, 2.0),
        (10, "mod", 3, 1),
        (10, "%", 3, 1),
        (10, "//", 3, 3),
        (10, "intdiv", 3, 3),
        (50, "percentage", 200, 25.0),
        (10, "absdiff", 3, 7),
        (3, "absdiff", 10, 7),
    ]
)
def test_calculator_operations(a, op, b, expected):
    """Test calculator performs operations correctly."""
    calc = Calculator()
    result = calc.calculate(a, op, b)
    assert result == expected


def test_calculator_adds_to_history():
    """Test that calculations are added to history."""
    calc = Calculator()
    calc.calculate(5, "+", 3)
    calc.calculate(10, "*", 2)
    
    assert not calc.history.is_empty()
    last_two = calc.history.last(2)
    assert len(last_two) == 2


def test_calculator_invalid_operation():
    """Test that invalid operations raise error."""
    calc = Calculator()
    with pytest.raises(InvalidOperationError, match="Invalid operation"):
        calc.calculate(5, "invalid", 3)


def test_calculator_division_by_zero():
    """Test that division by zero raises error."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.calculate(10, "/", 0)


def test_calculator_with_existing_history():
    """Test calculator can use existing history."""
    history = History.empty()
    history.add(datetime.now(), "1 + 1", 2)
    
    calc = Calculator(history=history)
    calc.calculate(5, "+", 3)
    
    last_two = calc.history.last(2)
    assert len(last_two) == 2


def test_observer_attach():
    """Test that observers can be attached."""
    calc = Calculator()
    observer = LoggingObserver()
    
    calc.attach(observer)
    assert observer in calc._observers


def test_observer_detach():
    """Test that observers can be detached."""
    calc = Calculator()
    observer = LoggingObserver()
    
    calc.attach(observer)
    calc.detach(observer)
    assert observer not in calc._observers

def test_logging_observer_logs_calculation(tmp_path):
    """Test that LoggingObserver writes to log file."""
    log_file = tmp_path / "test.log"
    calc = Calculator()
    observer = LoggingObserver(str(log_file))
    
    calc.attach(observer)
    calc.calculate(5, "+", 3)
    
    # Close handler to flush content to file
    observer.handler.close()
    
    assert log_file.exists()
    log_content = log_file.read_text()
    assert "Calculation:" in log_content
    assert "5 + 3 = 8" in log_content


def test_autosave_observer_saves_history(tmp_path):
    """Test that AutoSaveObserver saves history to CSV."""
    csv_file = tmp_path / "history.csv"
    calc = Calculator()
    observer = AutoSaveObserver(calc.history, str(csv_file))
    
    calc.attach(observer)
    calc.calculate(5, "+", 3)
    
    assert csv_file.exists()
    csv_content = csv_file.read_text()
    assert "5 + 3" in csv_content
    assert "8" in csv_content


def test_multiple_observers():
    """Test that multiple observers can be attached and notified."""
    calc = Calculator()
    log_observer = LoggingObserver()
    
    calc.attach(log_observer)
    
    # Should not raise error
    calc.calculate(5, "+", 3)
    assert len(calc._observers) == 1


def test_calculator_expression_format():
    """Test that expressions are formatted correctly in history."""
    calc = Calculator()
    calc.calculate(5, "+", 3)
    
    last = calc.history.last(1)
    assert len(last) == 1
    assert "5 + 3" in str(last.iloc[0])


@pytest.mark.parametrize(
    "a, op, b",
    [
        (10, "/", 0),
        (10, "mod", 0),
        (10, "//", 0),
        (50, "percentage", 0),
    ]
)
def test_calculator_zero_errors(a, op, b):
    """Test that operations handle zero divisor correctly."""
    calc = Calculator()
    with pytest.raises(ZeroDivisionError):
        calc.calculate(a, op, b)


def test_calculator_root_edge_cases():
    """Test root operation edge cases."""
    calc = Calculator()
    
    # Zeroth root should raise error
    with pytest.raises(ZeroDivisionError):
        calc.calculate(9, "root", 0)
    
    # Even root of negative should raise error
    with pytest.raises(ValueError):
        calc.calculate(-9, "root", 2)
