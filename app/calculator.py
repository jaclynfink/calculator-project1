from abc import ABC, abstractmethod
import logging
from datetime import datetime

from .history import History
from .operations import OperationFactory
from .input_validators import InputValidator
from .exceptions import ValidationError, InvalidOperationError, OperationError
from .logger import get_logger


class Observer(ABC):
    
    @abstractmethod
    def update(self, timestamp, expression, result):
        """Called when a new calculation is performed."""
        pass


class LoggingObserver(Observer):
    """Writes each calculation to a log file."""
    
    def __init__(self, log_file="calculator.log"):
        self.log_file = log_file
        # Use unique logger name based on file path
        logger_name = f"CalculatorLog_{id(self)}"
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        # Stop propagation to avoid pytest conflicts
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
        self.logger = get_logger()
        self.logger.info("Calculator initialized")
    
    def attach(self, observer):
        """Register an observer."""
        if observer not in self._observers:
            self._observers.append(observer)
            self.logger.log_observer_attached(observer.__class__.__name__)
    
    def detach(self, observer):
        """Unregister an observer."""
        if observer in self._observers:
            self._observers.remove(observer)
            self.logger.log_observer_detached(observer.__class__.__name__)
    
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
            # Log input received
            self.logger.log_input_received(a, operation_token, b)
            
            # Validate operation token
            operation_token = self.validator.validate_operation_token(operation_token)
            
            # Validate operands
            a, b = self.validator.validate_operands(a, b)
            
            # Get the operation from factory
            operation = OperationFactory.create(operation_token)
            self.logger.log_operation_created(operation_token)
            
            # Execute the operation
            result = operation.execute(a, b)
            
            # Round result to configured precision
            result = self.validator.round_result(result)
            
            # Create timestamp and expression
            timestamp = datetime.now()
            expression = f"{a} {operation.symbol} {b}"
            
            # Add to history
            self.history.add(timestamp, expression, result)
            
            # Log successful calculation
            self.logger.log_calculation(a, operation.symbol, b, result)
            
            # Notify observers
            self._notify_observers(timestamp, expression, result)
            
            return result
            
        except ZeroDivisionError as e:
            # Log and re-raise ZeroDivisionError as-is for specific handling
            self.logger.log_division_by_zero(a, operation_token, b)
            raise
        except InvalidOperationError as e:
            # Log invalid operation error
            self.logger.log_invalid_operation(operation_token)
            raise
        except ValidationError as e:
            # Log validation error
            self.logger.log_validation_error(f"{a}, {b}", str(e))
            raise
        except (ValueError, ArithmeticError) as e:
            # Convert other arithmetic errors to OperationError
            self.logger.log_operation_error(operation_token, str(e))
            raise OperationError(f"Operation failed: {str(e)}") from e
        except Exception as e:
            # Log any unexpected exceptions
            self.logger.log_exception(e, context="calculate method")
            raise
        
        return result