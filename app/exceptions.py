class InvalidOperationError(Exception):
    """Raised when user provides an invalid operation token."""
    pass

class UndoRedoError(Exception):
    """Raised when undo or redo operation cannot be performed."""
    pass

class HistoryError(Exception):
    """Raised when there is an error with history operations."""
    pass