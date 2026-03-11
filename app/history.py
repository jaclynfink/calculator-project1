from pathlib import Path
import pandas as pd
from datetime import datetime
from .exceptions import HistoryError, DataError
from .logger import get_logger


class Calculation:
    """
    Represents a single calculation with operation, operands, and result.
    """
    
    def __init__(self, timestamp, operation, operand1, operand2, result):
        """
        Create a Calculation instance.
        
        Args:
            timestamp: When the calculation was performed
            operation: Operation symbol (e.g., '+', '-', '*')
            operand1: First operand
            operand2: Second operand
            result: Calculation result
        """
        self.timestamp = timestamp if isinstance(timestamp, datetime) else datetime.fromisoformat(str(timestamp))
        self.operation = operation
        self.operand1 = float(operand1)
        self.operand2 = float(operand2)
        self.result = float(result)
    
    def __str__(self):
        """Return string representation of calculation."""
        return f"{self.operand1} {self.operation} {self.operand2} = {self.result}"
    
    def __repr__(self):
        """Return detailed representation."""
        return f"Calculation(timestamp={self.timestamp}, operation='{self.operation}', operand1={self.operand1}, operand2={self.operand2}, result={self.result})"


class History:
    """
    Stores calculation history in a pandas DataFrame
    
    Each row contains:
    - timestamp: when the calculation was done
    - operation: the operation symbol (e.g., '+', '-', '*')
    - operand1: first operand
    - operand2: second operand
    - result: the answer
    """
    
    def __init__(self, dataframe=None):
        """
        Create a new History object.
        
        Args:
            dataframe: A pandas DataFrame with history
        """
        self.logger = get_logger()
        if dataframe is None:
            #Create new DataFrame
            self.df = pd.DataFrame(columns=["timestamp", "operation", "operand1", "operand2", "result"])
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
    
    def add(self, timestamp, operation, operand1, operand2, result):
        """
        Add a new calculation to the history.
        
        Args:
            timestamp: When the calculation was done
            operation: Operation symbol (e.g., '+', '-', '*')
            operand1: First operand
            operand2: Second operand
            result: The answer
        """
        # Create a dictionary
        new_row = {
            "timestamp": timestamp,
            "operation": operation,
            "operand1": operand1,
            "operand2": operand2,
            "result": result
        }
        
        # Convert to DataFrame
        new_df = pd.DataFrame([new_row])
        
        # Avoid FutureWarning by checking if df is empty first
        if self.df.empty:
            self.df = new_df
        else:
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
            
            # Log successful save
            self.logger.log_history_saved(path)
            
        except PermissionError as e:
            self.logger.log_file_error(path, "Permission denied")
            raise DataError(
                f"Permission denied: Cannot write to '{path}'. "
                f"Please check file permissions."
            ) from e
        except OSError as e:
            self.logger.log_file_error(path, f"File system error: {str(e)}")
            raise DataError(
                f"File system error: Cannot save history to '{path}'. "
                f"Error: {str(e)}"
            ) from e
        except Exception as e:
            self.logger.log_exception(e, context=f"saving history to {path}")
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
        logger = get_logger()
        file_path = Path(path)
        
        # Check if file exists
        if not file_path.exists():
            logger.log_file_not_found(path)
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
            logger.log_exception(e, context=f"loading history from {path}")
            raise DataError(
                f"Unexpected error while loading history from '{path}': {str(e)}"
            )
        
        # Validate columns
        required_columns = {"timestamp", "operation", "operand1", "operand2", "result"}
        if not required_columns.issubset(set(df.columns)):
            missing = required_columns - set(df.columns)
            logger.log_data_error("load_csv", f"Missing columns: {missing}")
            raise DataError(
                f"Invalid CSV format: The file '{path}' is missing required columns: {missing}. "
                f"Expected columns: timestamp, operation, operand1, operand2, result."
            )
        
        # Log successful load
        logger.log_history_loaded(path, len(df))
        
        return cls(dataframe=df[list(required_columns)].copy())
    
    def to_calculations(self):
        """
        Convert history DataFrame to a list of Calculation instances.
        
        Returns:
            List of Calculation objects, one for each history entry
        """
        calculations = []
        for _, row in self.df.iterrows():
            calc = Calculation(
                timestamp=row['timestamp'],
                operation=row['operation'],
                operand1=row['operand1'],
                operand2=row['operand2'],
                result=row['result']
            )
            calculations.append(calc)
        return calculations
    
    @classmethod
    def from_calculations(cls, calculations):
        """
        Create a History object from a list of Calculation instances.
        
        Args:
            calculations: List of Calculation objects
            
        Returns:
            A History object containing the calculations
        """
        if not calculations:
            return cls.empty()
        
        data = [
            {
                "timestamp": calc.timestamp,
                "operation": calc.operation,
                "operand1": calc.operand1,
                "operand2": calc.operand2,
                "result": calc.result
            }
            for calc in calculations
        ]
        
        df = pd.DataFrame(data)
        return cls(dataframe=df)