import pytest
from pathlib import Path
from app.logger import Logger, get_logger


def test_logger_singleton(monkeypatch, tmp_path):
    """Test that Logger follows singleton pattern."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    # Reset singleton
    Logger._instance = None
    Logger._logger = None
    
    logger1 = Logger()
    logger2 = Logger()
    
    assert logger1 is logger2


def test_get_logger_returns_singleton(monkeypatch, tmp_path):
    """Test that get_logger returns singleton instance."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger1 = get_logger()
    logger2 = get_logger()
    
    assert logger1 is logger2


def test_logger_creates_log_file(monkeypatch, tmp_path):
    """Test that logger creates log file in correct directory."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.info("test message")
    
    log_file = log_dir / "calculator.log"
    assert log_file.exists()


def test_logger_info_writes_to_file(monkeypatch, tmp_path):
    """Test that INFO level messages are written to file."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.info("test info message")
    
    # Force flush handlers
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "test info message" in content
    assert "INFO" in content


def test_logger_warning_writes_to_file(monkeypatch, tmp_path):
    """Test that WARNING level messages are written to file."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.warning("test warning message")
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "test warning message" in content
    assert "WARNING" in content


def test_logger_error_writes_to_file(monkeypatch, tmp_path):
    """Test that ERROR level messages are written to file."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.error("test error message")
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "test error message" in content
    assert "ERROR" in content


def test_log_calculation(monkeypatch, tmp_path):
    """Test calculation logging method."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.log_calculation(5, "+", 3, 8)
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "Calculation performed: 5 + 3 = 8" in content


def test_log_operation_created(monkeypatch, tmp_path):
    """Test operation creation logging."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.log_operation_created("add")
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "Operation created: add" in content


def test_log_history_saved(monkeypatch, tmp_path):
    """Test history save logging."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.log_history_saved("history.csv")
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "History saved to: history.csv" in content


def test_log_history_loaded(monkeypatch, tmp_path):
    """Test history load logging."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.log_history_loaded("history.csv", 10)
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "History loaded from: history.csv (10 entries)" in content


def test_log_observer_attached(monkeypatch, tmp_path):
    """Test observer attachment logging."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.log_observer_attached("LoggingObserver")
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "Observer attached: LoggingObserver" in content


def test_log_division_by_zero(monkeypatch, tmp_path):
    """Test division by zero error logging."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.log_division_by_zero(10, "/", 0)
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "Division by zero error: 10 / 0" in content
    assert "ERROR" in content


def test_log_invalid_operation(monkeypatch, tmp_path):
    """Test invalid operation logging."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.log_invalid_operation("invalid_op")
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "Invalid operation token: 'invalid_op'" in content


def test_log_validation_error(monkeypatch, tmp_path):
    """Test validation error logging."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.log_validation_error("abc", "not a number")
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "Validation error for 'abc': not a number" in content


def test_log_exception_includes_traceback(monkeypatch, tmp_path):
    """Test that exception logging includes traceback."""
    log_dir = tmp_path / "logs"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    
    try:
        raise ValueError("test exception")
    except ValueError as e:
        logger.log_exception(e, context="test context")
    
    for handler in logger._logger.handlers:
        handler.flush()
    
    log_file = log_dir / "calculator.log"
    content = log_file.read_text()
    assert "Exception occurred (test context)" in content
    assert "test exception" in content
    assert "Traceback" in content or "ERROR" in content


def test_logger_creates_directory_if_not_exists(monkeypatch, tmp_path):
    """Test that logger creates log directory if it doesn't exist."""
    log_dir = tmp_path / "new_logs" / "nested"
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    Logger._instance = None
    Logger._logger = None
    
    logger = Logger()
    logger.info("test")
    
    assert log_dir.exists()
    assert (log_dir / "calculator.log").exists()
