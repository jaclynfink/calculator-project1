import pandas as pd
import pytest
from app.calculator_memento import HistoryCaretaker, HistoryMemento
from app.exceptions import UndoRedoError

def test_caretaker_initial_state_rules():
    c = HistoryCaretaker()

    c.push(HistoryMemento(pd.DataFrame([{"a":1}])))
    assert c.can_undo() is False
    assert c.can_redo() is False

def test_undo_redo_flow():
    c = HistoryCaretaker()
    c.push(HistoryMemento(pd.DataFrame([{"v":0}])))
    c.push(HistoryMemento(pd.DataFrame([{"v":1}])))
    c.push(HistoryMemento(pd.DataFrame([{"v":2}])))
    assert c.can_undo() is True

    m = c.undo()
    assert m.df.iloc[0]["v"] == 1
    assert c.can_redo() is True

    m2 = c.redo()
    assert m2.df.iloc[0]["v"] == 2

def test_undo_when_nothing_to_undo():
    c = HistoryCaretaker()
    c.push(HistoryMemento(pd.DataFrame()))
    with pytest.raises(UndoRedoError, match="Nothing to undo"):
        c.undo()

def test_redo_when_nothing_to_redo():
    c = HistoryCaretaker()
    c.push(HistoryMemento(pd.DataFrame()))
    c.push(HistoryMemento(pd.DataFrame([{"v":1}])))
    c.undo()
    c.redo()
    with pytest.raises(UndoRedoError, match="Nothing to redo"):
        c.redo()