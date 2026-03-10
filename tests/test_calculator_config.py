import pytest
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigError

def test_config_defaults(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    cfg = CalculatorConfig.load()
    assert cfg.auto_save is True
    assert cfg.max_history_size == 1000
    assert cfg.precision == 10
    assert cfg.max_input_value == 1000000
    assert cfg.default_encoding == "utf-8"

@pytest.mark.parametrize("val", ["1","true","YES","on","y"])
def test_config_autosave_true(monkeypatch, tmp_path, val):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", val)
    cfg = CalculatorConfig.load()
    assert cfg.auto_save is True

@pytest.mark.parametrize("val", ["0","false","No","off","n"])
def test_config_autosave_false(monkeypatch, tmp_path, val):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", val)
    cfg = CalculatorConfig.load()
    assert cfg.auto_save is False

def test_config_invalid_bool(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", "maybe")
    with pytest.raises(ConfigError, match="Invalid boolean"):
        CalculatorConfig.load()

def test_config_empty_log_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", "  ")
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    with pytest.raises(ConfigError, match="cannot be empty"):
        CalculatorConfig.load()

def test_config_empty_history_dir(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", "  ")
    with pytest.raises(ConfigError, match="cannot be empty"):
        CalculatorConfig.load()

def test_config_custom_values(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "custom_logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "custom_history"))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "500")
    monkeypatch.setenv("CALCULATOR_PRECISION", "5")
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "999999")
    monkeypatch.setenv("CALCULATOR_DEFAULT_ENCODING", "latin-1")
    
    cfg = CalculatorConfig.load()
    assert cfg.max_history_size == 500
    assert cfg.precision == 5
    assert cfg.max_input_value == 999999
    assert cfg.default_encoding == "latin-1"

def test_config_invalid_max_history_size(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "not_a_number")
    with pytest.raises(ConfigError, match="must be an integer"):
        CalculatorConfig.load()

def test_config_negative_max_history_size(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_HISTORY_SIZE", "-10")
    with pytest.raises(ConfigError, match="must be positive"):
        CalculatorConfig.load()

def test_config_invalid_precision(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_PRECISION", "abc")
    with pytest.raises(ConfigError, match="must be an integer"):
        CalculatorConfig.load()

def test_config_invalid_max_input_value(monkeypatch, tmp_path):
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    monkeypatch.setenv("CALCULATOR_MAX_INPUT_VALUE", "xyz")
    with pytest.raises(ConfigError, match="must be a number"):
        CalculatorConfig.load()

def test_config_directories_created(monkeypatch, tmp_path):
    log_dir = tmp_path / "new_logs"
    history_dir = tmp_path / "new_history"
    
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(log_dir))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(history_dir))
    
    cfg = CalculatorConfig.load()
    
    assert log_dir.exists()
    assert history_dir.exists()

def test_config_backward_compatibility(monkeypatch, tmp_path):
    """Test that legacy properties work for backward compatibility."""
    monkeypatch.setenv("CALCULATOR_LOG_DIR", str(tmp_path / "logs"))
    monkeypatch.setenv("CALCULATOR_HISTORY_DIR", str(tmp_path / "history"))
    
    cfg = CalculatorConfig.load()
    
    # Legacy properties should still work
    assert cfg.autosave == cfg.auto_save
    assert "calculator_history.csv" in cfg.history_file