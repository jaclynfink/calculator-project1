from pathlib import Path
import pandas as pd
from .exceptions import HistoryError, DataError


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
    
    def save_csv(self, path, encoding='utf-8'):
        """
        Save history to a CSV file with robust error handling.
        
        Args:
            path: File path to save the CSV
            encoding: File encoding (default: utf-8)
            
        Raises:
            DataError: If saving fails
        """
        try:
            # Create parent directory if it doesn't exist
            file_path = Path(path)
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save to CSV
            self.df.to_csv(path, index=False, encoding=encoding)
            
        except PermissionError as e:
            raise DataError(
                f"Permission denied: Cannot write to '{path}'. "
                f"Please check file permissions."
            ) from e
        except OSError as e:
            raise DataError(
                f"File system error: Cannot save history to '{path}'. "
                f"Error: {str(e)}"
            ) from e
        except Exception as e:
            raise DataError(
                f"Unexpected error while saving history to '{path}': {str(e)}"
            ) from e
    
    @classmethod
    def load_csv(cls, path, encoding='utf-8'):
        """
        Load history from a CSV file with robust error handling.
        
        Args:
            path: File path to load from
            encoding: File encoding (default: utf-8)
            
        Returns:
            A History object with loaded data
            
        Raises:
            DataError: If loading fails
        """
        file_path = Path(path)
        
        # Check if file exists
        if not file_path.exists():
            return cls.empty()
        
        try:
            # Read CSV file
            df = pd.read_csv(path, encoding=encoding)
            
        except pd.errors.EmptyDataError:
            raise DataError(
                f"Empty data: The file '{path}' is empty or contains no data."
            )
        except pd.errors.ParserError as e:
            raise DataError(
                f"Parse error: Cannot read '{path}' as CSV. "
                f"The file may be corrupted or have invalid formatting. Error: {str(e)}"
            )
        except UnicodeDecodeError as e:
            raise DataError(
                f"Encoding error: Cannot read '{path}' with {encoding} encoding. "
                f"Try a different encoding or check if the file is corrupted."
            )
        except FileNotFoundError:
            raise DataError(
                f"File not found: '{path}' does not exist."
            )
        except PermissionError:
            raise DataError(
                f"Permission denied: Cannot read from '{path}'. "
                f"Please check file permissions."
            )
        except Exception as e:
            raise DataError(
                f"Unexpected error while loading history from '{path}': {str(e)}"
            )
        
        # Validate columns
        required_columns = {"timestamp", "expression", "result"}
        if not required_columns.issubset(set(df.columns)):
            missing = required_columns - set(df.columns)
            raise DataError(
                f"Invalid CSV format: The file '{path}' is missing required columns: {missing}. "
                f"Expected columns: timestamp, expression, result."
            )
        
        return cls(dataframe=df[list(required_columns)].copy())