import pandas as pd
from .exceptions import UndoRedoError


class HistoryMemento:
    """
    A snapshot of the History at a specific point in time.
    """
    
    def __init__(self, dataframe):
        """
        Args:
            dataframe: The pandas DataFrame snapshot to save
        """
        self.df = dataframe


class HistoryCaretaker:
    """
    - When you do something: Save current state to undo stack
    - When you undo: Move from undo stack to redo stack
    - When you redo: Move from redo stack to undo stack
    """
    
    def __init__(self):
        """Create empty undo and redo stacks."""
        self._undo_stack = []  # Stores past snapshots
        self._redo_stack = []  # Stores future snapshots
    
    def push(self, memento):
        """
        Save a new snapshot to the undo stack.
        
        Args:
            memento: The snapshot to save
        """
        self._undo_stack.append(memento)
        # Clear redo stack
        self._redo_stack.clear()
    
    def can_undo(self):
        """
        Check if we can undo.
        
        Returns:
            True if undo is possible, False otherwise
        """
        return len(self._undo_stack) > 1
    
    def can_redo(self):
        """
        Check if we can redo.
        
        Returns:
            True if redo is possible, False otherwise
        """
        return len(self._redo_stack) > 0
    
    def undo(self):
        """
        Go back to the previous snapshot.
        
        Returns:
            The previous snapshot (memento)
        """
        if not self.can_undo():
            raise UndoRedoError("ERROR: Nothing to undo")
        
        # Remove current snapshot and save to redo stack
        current_snapshot = self._undo_stack.pop()
        self._redo_stack.append(current_snapshot)
        
        # Return the previous snapshot (now at top of undo stack)
        return self._undo_stack[-1]
    
    def redo(self):
        """
        Go forward to the next snapshot.
        
        Returns:
            The next snapshot (memento)
        """
        if not self.can_redo():
            raise UndoRedoError("ERROR: Nothing to redo")
        
        # Get the next snapshot from redo stack
        next_snapshot = self._redo_stack.pop()
        
        # Put it back on the undo stack
        self._undo_stack.append(next_snapshot)
        
        return next_snapshot