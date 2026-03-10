import pandas as pd
import pytest
from app.history import History
from app.exceptions import HistoryError, DataError

def test_history_empty():
    h = History.empty()
    assert h.is_empty()
    assert list(h.df.columns) == ["timestamp","expression","result"]

def test_history_add_and_last():
    h = History.empty()
    h.add("t1", "1 + 1", 2)
    h.add("t2", "2 + 2", 4)
    assert not h.is_empty()
    last1 = h.last(1)
    assert len(last1) == 1
    assert last1.iloc[0]["expression"] == "2 + 2"

def test_history_last_nonpositive_returns_empty_copy():
    h = History.empty()
    h.add("t1","x",1)
    out = h.last(0)
    assert out.empty

def test_history_clear():
    h = History.empty()
    h.add("t1","x",1)
    h.clear()
    assert h.is_empty()

def test_history_save_and_load_roundtrip(tmp_path):
    path = tmp_path / "hist.csv"
    h = History.empty()
    h.add("t1","1 + 1",2)
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
    h.add("t1", "1 + 1", 2)
    h.save_csv(str(nested_path))
    assert nested_path.exists()


def test_history_save_with_encoding(tmp_path):
    """Test saving with custom encoding."""
    path = tmp_path / "encoded.csv"
    h = History.empty()
    h.add("t1", "1 + 1", 2)
    h.save_csv(str(path), encoding='latin-1')
    assert path.exists()


def test_history_load_with_encoding(tmp_path):
    """Test loading with custom encoding."""
    path = tmp_path / "encoded.csv"
    h = History.empty()
    h.add("t1", "1 + 1", 2)
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