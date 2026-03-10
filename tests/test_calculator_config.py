import pytest
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigError

def test_config_defaults(monkeypatch, tmp_path):
    monkeypatch.setenv("CALC_HISTORY_FILE", str(tmp_path / "h.csv"))
    cfg = CalculatorConfig.load()
    assert cfg.autosave is True
    assert cfg.strategy == "EAFP"

@pytest.mark.parametrize("val", ["1","true","YES","on","y"])
def test_config_autosave_true(monkeypatch, tmp_path, val):
    monkeypatch.setenv("CALC_HISTORY_FILE", str(tmp_path / "h.csv"))
    monkeypatch.setenv("CALC_AUTOSAVE", val)
    cfg = CalculatorConfig.load()
    assert cfg.autosave is True

@pytest.mark.parametrize("val", ["0","false","No","off","n"])
def test_config_autosave_false(monkeypatch, tmp_path, val):
    monkeypatch.setenv("CALC_HISTORY_FILE", str(tmp_path / "h.csv"))
    monkeypatch.setenv("CALC_AUTOSAVE", val)
    cfg = CalculatorConfig.load()
    assert cfg.autosave is False

def test_config_invalid_bool(monkeypatch, tmp_path):
    monkeypatch.setenv("CALC_HISTORY_FILE", str(tmp_path / "h.csv"))
    monkeypatch.setenv("CALC_AUTOSAVE", "maybe")
    with pytest.raises(ConfigError, match="Invalid boolean"):
        CalculatorConfig.load()

def test_config_invalid_strategy(monkeypatch, tmp_path):
    monkeypatch.setenv("CALC_HISTORY_FILE", str(tmp_path / "h.csv"))
    monkeypatch.setenv("CALC_STRATEGY", "FAST")
    with pytest.raises(ConfigError, match="CALC_STRATEGY"):
        CalculatorConfig.load()

def test_config_empty_history_file(monkeypatch):
    monkeypatch.setenv("CALC_HISTORY_FILE", "  ")
    with pytest.raises(ConfigError, match="cannot be empty"):
        CalculatorConfig.load()