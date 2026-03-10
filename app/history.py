from pathlib import Path
import pandas as pd
from .exceptions import HistoryError


class History:
    """
    Stores calculation history in a pandas DataFrame
    
    Each row contains:
    - timestamp: when the calculation was done
    - expression: what was calculated (like "5 + 3")
    - result: the answer
    """
    
    def __init__(self, dataframe=None):
        """
        Create a new History object.
        
        Args:
            dataframe: A pandas DataFrame with history
        """
        if dataframe is None:
            #Create new DataFrame
            self.df = pd.DataFrame(columns=["timestamp", "expression", "result"])
        else:
            self.df = dataframe
    
    @classmethod
    def empty(cls):
        """
        Create a new empty history.
        
        Returns:
            A History object with no calculations
        """
        return cls(dataframe=None)
    
    def add(self, timestamp, expression, result):
        """
        Add a new calculation to the history.
        
        Args:
            timestamp: When the calculation was done
            expression: The calculation string
            result: The answer
        """
        # Create a dictionary
        new_row = {
            "timestamp": timestamp,
            "expression": expression,
            "result": result
        }
        
        # Convert to DataFrame
        new_df = pd.DataFrame([new_row])
        self.df = pd.concat([self.df, new_df], ignore_index=True)
    
    def clear(self):
        """Delete all history entries."""
        self.df = self.df.iloc[0:0].copy()
    
    def is_empty(self):
        """
        Check if there are any calculations in the history.
        
        Returns:
            True if history is empty, False otherwise
        """
        return self.df.empty
    
    def last(self, n=10):
        """
        Get the last n calculations from history.
        
        Args:
            n: Number of recent calculations to return (default 10)
            
        Returns:
            A DataFrame with the last n calculations
        """
        if n <= 0:
            # Return empty DataFrame if n is 0 or negative
            return self.df.iloc[0:0].copy()
        
        return self.df.tail(n).copy()
    
    def save_csv(self, path):
        """
        Save history to a CSV file
        
        Args:
            path: File path to save the CSV

        """
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            
            self.df.to_csv(path, index=False)
        except Exception as e:
            raise HistoryError(f"ERROR: Failed to save history: {e}") from e
    
    @classmethod
    def load_csv(cls, path):
        """
        Load history from a CSV file.
        
        Args:
            path: File path to load from
            
        Returns:
            A History object with loaded data
        """
        # Check if file exists
        file_path = Path(path)
        if not file_path.exists():
            return cls.empty()
        
        try:
            df = pd.read_csv(path)
        except Exception as e:
            raise HistoryError(f"ERROR: Failed to load history: {e}") from e
        
        # Check that the file has the right columns
        required_columns = {"timestamp", "expression", "result"}
        if not required_columns.issubset(set(df.columns)):
            raise HistoryError("ERROR: History CSV missing required columns")
        
        return cls(dataframe=df[list(required_columns)].copy())