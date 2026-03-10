from abc import ABC, abstractmethod
import logging
from datetime import datetime

from .history import History
from .operations import OperationFactory
from .input_validators import InputValidator
from .exceptions import ValidationError, InvalidOperationError, OperationError


class Observer(ABC):
    
    @abstractmethod
    def update(self, timestamp, expression, result):
        """Called when a new calculation is performed."""
        pass


class LoggingObserver(Observer):
    """Writes each calculation to a log file."""
    
    def __init__(self, log_file="calculator.log"):
        self.log_file = log_file
        # Use unique logger name based on file path to avoid conflicts
        logger_name = f"CalculatorLog_{id(self)}"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        # Prevent propagation to avoid pytest capture conflicts
        self.logger.propagate = False
        
        self.handler = logging.FileHandler(log_file)
        self.handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
    
    def update(self, timestamp, expression, result):
        self.logger.info(f"Calculation: {expression} = {result}")


class AutoSaveObserver(Observer):
    """Automatically saves calculation history to CSV."""
    
    def __init__(self, history, history_file):
        self.history = history
        self.history_file = history_file
    
    def update(self, timestamp, expression, result):
        self.history.save_csv(self.history_file)


class Calculator:
    def __init__(self, history=None, validator=None):
        self.history = history or History.empty()
        self.validator = validator or InputValidator()
        self._observers = []
    
    def attach(self, observer):
        """Register an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer):
        """Unregister an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def _notify_observers(self, timestamp, expression, result):
        """Notify all observers of a new calculation."""
        for observer in self._observers:
            observer.update(timestamp, expression, result)
    
    def calculate(self, a, operation_token, b):
        """
        Perform a calculation with input validation.
        
        Args:
            a: First operand
            operation_token: Operation token (e.g., "+", "add", "*")
            b: Second operand
            
        Returns:
            The calculation result
            
        Raises:
            ValidationError: If inputs are invalid
            InvalidOperationError: If operation token is invalid
            OperationError: If operation cannot be performed (e.g., division by zero)
        """
        try:
            # Validate operation token
            operation_token = self.validator.validate_operation_token(operation_token)
            
            # Validate operands
            a, b = self.validator.validate_operands(a, b)
            
            # Get the operation from factory
            operation = OperationFactory.create(operation_token)
            
            # Execute the operation
            result = operation.execute(a, b)
            
            # Round result to configured precision
            result = self.validator.round_result(result)
            
            # Create timestamp and expression
            timestamp = datetime.now()
            expression = f"{a} {operation.symbol} {b}"
            
            # Add to history
            self.history.add(timestamp, expression, result)
            
            # Notify observers
            self._notify_observers(timestamp, expression, result)
            
            return result
            
        except ZeroDivisionError:
            # Re-raise ZeroDivisionError as-is for specific handling
            raise
        except (ValueError, ArithmeticError) as e:
            # Convert other arithmetic errors to OperationError
            raise OperationError(f"Operation failed: {str(e)}") from e
        
        return result