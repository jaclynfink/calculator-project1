import pytest
from app.input_validators import InputValidator
from app.exceptions import ValidationError
from app.calculator_config import CalculatorConfig


def test_validate_number_valid_int(monkeypatch, tmp_path):
    """Test that valid integers are accepted."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    assert validator.validate_number(5) == 5.0


def test_validate_number_valid_float(monkeypatch, tmp_path):
    """Test that valid floats are accepted."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    assert validator.validate_number(3.14) == 3.14


def test_validate_number_string_number(monkeypatch, tmp_path):
    """Test that numeric strings are converted."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    assert validator.validate_number("42") == 42.0
    assert validator.validate_number("3.14") == 3.14


def test_validate_number_invalid_string(monkeypatch, tmp_path):
    """Test that non-numeric strings are rejected."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    with pytest.raises(ValidationError, match="not a valid number"):
        validator.validate_number("abc")


def test_validate_number_exceeds_max(monkeypatch, tmp_path):
    """Test that numbers exceeding max value are rejected."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "100")
    validator = InputValidator()
    with pytest.raises(ValidationError, match="exceeds maximum"):
        validator.validate_number(101)


def test_validate_number_negative_exceeds_max(monkeypatch, tmp_path):
    """Test that negative numbers exceeding max value are rejected."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "100")
    validator = InputValidator()
    with pytest.raises(ValidationError, match="exceeds maximum"):
        validator.validate_number(-101)


def test_validate_number_infinity(monkeypatch, tmp_path):
    """Test that infinity is rejected."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    with pytest.raises(ValidationError, match="not a finite number"):
        validator.validate_number(float('inf'))


def test_validate_number_nan(monkeypatch, tmp_path):
    """Test that NaN is rejected."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    with pytest.raises(ValidationError, match="not a finite number"):
        validator.validate_number(float('nan'))


def test_validate_operands_both_valid(monkeypatch, tmp_path):
    """Test that two valid operands are accepted."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    a, b = validator.validate_operands(5, 3)
    assert a == 5.0
    assert b == 3.0


def test_validate_operands_first_invalid(monkeypatch, tmp_path):
    """Test that invalid first operand is rejected."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    with pytest.raises(ValidationError, match="first operand"):
        validator.validate_operands("abc", 3)


def test_validate_operands_second_invalid(monkeypatch, tmp_path):
    """Test that invalid second operand is rejected."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    with pytest.raises(ValidationError, match="second operand"):
        validator.validate_operands(5, "xyz")


def test_validate_operation_token_valid(monkeypatch, tmp_path):
    """Test that valid operation tokens are accepted."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    assert validator.validate_operation_token("+") == "+"
    assert validator.validate_operation_token("  add  ") == "add"


def test_validate_operation_token_empty(monkeypatch, tmp_path):
    """Test that empty operation token is rejected."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    with pytest.raises(ValidationError, match="cannot be empty"):
        validator.validate_operation_token("")


def test_validate_operation_token_none(monkeypatch, tmp_path):
    """Test that None operation token is rejected."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    validator = InputValidator()
    with pytest.raises(ValidationError, match="cannot be empty"):
        validator.validate_operation_token(None)


def test_round_result(monkeypatch, tmp_path):
    """Test that results are rounded to configured precision."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_PRECISION", "2")
    validator = InputValidator()
    assert validator.round_result(3.14159) == 3.14


def test_round_result_zero_precision(monkeypatch, tmp_path):
    """Test rounding with zero precision."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_PRECISION", "0")
    validator = InputValidator()
    assert validator.round_result(3.7) == 4.0


def test_validator_with_custom_config(monkeypatch, tmp_path):
    """Test validator with custom configuration."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "50")
    
    config = CalculatorConfig.load()
    validator = InputValidator(config)
    
    # Should accept 50
    assert validator.validate_number(50) == 50.0
    
    # Should reject 51
    with pytest.raises(ValidationError):
        validator.validate_number(51)
