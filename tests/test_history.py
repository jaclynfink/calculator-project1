import pandas as pd
import pytest
from app.history import History
from app.exceptions import HistoryError, DataError

def test_history_empty():
    h = History.empty()
    assert h.is_empty()
    assert list(h.df.columns) == ["timestamp","operation","operand1","operand2","result"]

def test_history_add_and_last():
    h = History.empty()
    h.add("t1", "+", 1, 1, 2)
    h.add("t2", "+", 2, 2, 4)
    assert not h.is_empty()
    last1 = h.last(1)
    assert len(last1) == 1
    assert last1.iloc[0]["operation"] == "+"

def test_history_last_nonpositive_returns_empty_copy():
    h = History.empty()
    h.add("t1","+",1,2,3)
    out = h.last(0)
    assert out.empty

def test_history_clear():
    h = History.empty()
    h.add("t1","+",1,2,3)
    h.clear()
    assert h.is_empty()

def test_history_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "hist.csv"
    h = History.empty()
    h.add("t1","+",1,1,2)
    h.save_csv(str(path))
    h2 = History.load_csv(str(path))
    assert len(h2.df) == 1
    assert h2.df.iloc[0]["result"] == 2

def test_history_load_missing_file_returns_empty(tmp_path):
    path = tmp_path / "missing.csv"
    h = History.load_csv(str(path))
    assert h.is_empty()

def test_history_load_missing_columns(tmp_path):
    path = tmp_path / "bad.csv"
    pd.DataFrame([{"a":1}]).to_csv(path, index=False)
    with pytest.raises(DataError, match="missing required columns"):
        History.load_csv(str(path))


def test_history_load_empty_file(tmp_path):
    """Test loading an empty CSV file."""
    path = tmp_path / "empty.csv"
    path.write_text("")
    with pytest.raises(DataError, match="empty"):
        History.load_csv(str(path))


def test_history_save_creates_directory(tmp_path):
    """Test that save_csv creates parent directory."""
    nested_path = tmp_path / "nested" / "dir" / "hist.csv"
    h = History.empty()
    h.add("t1", "+", 1, 1, 2)
    h.save_csv(str(nested_path))
    assert nested_path.exists()


def test_history_save_with_encoding(tmp_path):
    """Test saving with custom encoding."""
    path = tmp_path / "encoded.csv"
    h = History.empty()
    h.add("t1", "+", 1, 1, 2)
    h.save_csv(str(path), encoding='latin-1')
    assert path.exists()


def test_history_load_with_encoding(tmp_path):
    """Test loading with custom encoding."""
    path = tmp_path / "encoded.csv"
    h = History.empty()
    h.add("t1", "+", 1, 1, 2)
    h.save_csv(str(path), encoding='latin-1')
    h2 = History.load_csv(str(path), encoding='latin-1')
    assert len(h2.df) == 1

def test_history_save_failure_raises(tmp_path, monkeypatch):
    h = History.empty()

    def boom(*args, **kwargs):
        raise RuntimeError("nope")
    monkeypatch.setattr(h.df, "to_csv", boom)
    with pytest.raises(DataError, match="Unexpected error"):
        h.save_csv(str(tmp_path / "x.csv"))

def test_history_load_failure_raises(tmp_path, monkeypatch):
    path = tmp_path / "x.csv"
    path.write_text("not,csv,\n1,2,3\n")

    import pandas as pd
    def boom(*args, **kwargs):
        raise RuntimeError("bad")
    monkeypatch.setattr(pd, "read_csv", boom)
    with pytest.raises(DataError, match="Unexpected error"):
        History.load_csv(str(path))

def test_history_save_permission_error(tmp_path, monkeypatch):
    """Test save with permission error."""
    h = History.empty()
    h.add("t1", "+", 1, 1, 2)
    
    def raise_permission(*args, **kwargs):
        raise PermissionError("Permission denied")
    
    monkeypatch.setattr(h.df, "to_csv", raise_permission)
    
    with pytest.raises(DataError, match="Permission denied"):
        h.save_csv(str(tmp_path / "test.csv"))

def test_history_save_os_error(tmp_path, monkeypatch):
    """Test save with OS error."""
    h = History.empty()
    h.add("t1", "+", 1, 1, 2)
    
    def raise_os_error(*args, **kwargs):
        raise OSError("Disk full")
    
    monkeypatch.setattr(h.df, "to_csv", raise_os_error)
    
    with pytest.raises(DataError, match="File system error"):
        h.save_csv(str(tmp_path / "test.csv"))

def test_history_load_unicode_error(tmp_path):
    """Test load with unicode decode error."""
    path = tmp_path / "bad_encoding.csv"
    # Write some binary data that won't decode as UTF-8
    path.write_bytes(b'\xff\xfe' + b'bad data')
    
    with pytest.raises(DataError, match="Encoding error"):
        History.load_csv(str(path))

def test_history_load_file_not_found_error(tmp_path):
    """Test load with file not found after checking existence."""
    import pandas as pd
    import unittest.mock as mock
    
    # Mock to simulate file disappearing between existence check and read
    def raise_file_not_found(*args, **kwargs):
        raise FileNotFoundError("File disappeared")
    
    with mock.patch('pandas.read_csv', side_effect=raise_file_not_found):
        # Create a dummy file so it passes existence check
        path = tmp_path / "test.csv"
        path.write_text("timestamp,operation,operand1,operand2,result\n")
        
        with pytest.raises(DataError, match="File not found"):
            History.load_csv(str(path))


def test_calculation_creation():
    """Test creating a Calculation instance."""
    from app.history import Calculation
    from datetime import datetime
    dt = datetime(2024, 1, 1, 12, 0, 0)
    calc = Calculation(dt, "+", 1.0, 2.0, 3.0)
    assert calc.timestamp == dt
    assert calc.operation == "+"
    assert calc.operand1 == 1.0
    assert calc.operand2 == 2.0
    assert calc.result == 3.0


def test_calculation_str():
    """Test Calculation string representation."""
    from app.history import Calculation
    from datetime import datetime
    dt = datetime(2024, 1, 1, 12, 0, 0)
    calc = Calculation(dt, "+", 1.0, 2.0, 3.0)
    assert str(calc) == "1.0 + 2.0 = 3.0"


def test_calculation_repr():
    """Test Calculation repr."""
    from app.history import Calculation
    from datetime import datetime
    dt = datetime(2024, 1, 1, 12, 0, 0)
    calc = Calculation(dt, "+", 1.0, 2.0, 3.0)
    result = repr(calc)
    assert "Calculation" in result
    assert "+" in result
    assert "1.0" in result
    assert "2.0" in result
    assert "3.0" in result


def test_history_to_calculations():
    """Test converting history to list of Calculation instances."""
    from app.history import Calculation
    from datetime import datetime
    h = History.empty()
    dt1 = datetime(2024, 1, 1, 12, 0, 0)
    dt2 = datetime(2024, 1, 1, 13, 0, 0)
    h.add(dt1, "+", 1.0, 2.0, 3.0)
    h.add(dt2, "*", 4.0, 5.0, 20.0)
    
    calcs = h.to_calculations()
    assert len(calcs) == 2
    assert isinstance(calcs[0], Calculation)
    assert calcs[0].operation == "+"
    assert calcs[0].operand1 == 1.0
    assert calcs[1].operation == "*"
    assert calcs[1].result == 20.0


def test_history_to_calculations_empty():
    """Test converting empty history to calculations."""
    h = History.empty()
    calcs = h.to_calculations()
    assert calcs == []


def test_history_from_calculations():
    """Test creating history from Calculation list."""
    from app.history import Calculation
    from datetime import datetime
    dt1 = datetime(2024, 1, 1, 12, 0, 0)
    dt2 = datetime(2024, 1, 1, 13, 0, 0)
    calcs = [
        Calculation(dt1, "+", 1.0, 2.0, 3.0),
        Calculation(dt2, "-", 10.0, 3.0, 7.0)
    ]
    
    h = History.from_calculations(calcs)
    assert len(h.df) == 2
    assert h.df.iloc[0]["operation"] == "+"
    assert h.df.iloc[0]["result"] == 3.0
    assert h.df.iloc[1]["operation"] == "-"
    assert h.df.iloc[1]["result"] == 7.0


def test_history_from_calculations_empty():
    """Test creating history from empty calculation list."""
    h = History.from_calculations([])
    assert h.is_empty()
