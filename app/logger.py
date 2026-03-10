import logging
from pathlib import Path
from datetime import datetime
from .calculator_config import CalculatorConfig


class Logger:
    """
    Comprehensive logging system for the calculator application.
    Logs events, errors, and calculation details
    """
    
    _instance = None
    _logger = None
    
    def __new__(cls):
        """Ensure only one logger instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the logger"""
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """Load the logger"""
        config = CalculatorConfig.load()
        
        # Create logger
        self._logger = logging.getLogger("CalculatorApp")
        self._logger.setLevel(logging.DEBUG)
        
        # Clear any existing handlers (for testing and reinitialization)
        self._logger.handlers.clear()
        
        # Create log directory and file path
        log_file = config.log_dir / "calculator.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # File handler - logs everything to file
        file_handler = logging.FileHandler(str(log_file))
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler - only warnings and errors to console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self._logger.addHandler(file_handler)
        self._logger.addHandler(console_handler)
    
    # INFO level methods
    def info(self, message):
        """Log an informational message."""
        self._logger.info(message)
    
    def log_calculation(self, operand1, operation, operand2, result):
        """
        Log a successful calculation.
        
        Args:
            operand1: First operand
            operation: Operation symbol/token
            operand2: Second operand
            result: Calculation result
        """
        self._logger.info(
            f"Calculation performed: {operand1} {operation} {operand2} = {result}"
        )
    
    def log_operation_created(self, operation_token):
        """Log when an operation is successfully created."""
        self._logger.info(f"Operation created: {operation_token}")
    
    def log_history_saved(self, path):
        """Log when history is saved."""
        self._logger.info(f"History saved to: {path}")
    
    def log_history_loaded(self, path, entries):
        """Log when history is loaded."""
        self._logger.info(f"History loaded from: {path} ({entries} entries)")
    
    def log_config_loaded(self):
        """Log when configuration is loaded."""
        self._logger.info("Configuration loaded successfully")
    
    def log_observer_attached(self, observer_name):
        """Log when an observer is attached."""
        self._logger.info(f"Observer attached: {observer_name}")
    
    def log_observer_detached(self, observer_name):
        """Log when an observer is detached."""
        self._logger.info(f"Observer detached: {observer_name}")
    
    # WARNING level methods
    def warning(self, message):
        """Log a warning message."""
        self._logger.warning(message)
    
    def log_validation_warning(self, issue):
        """Log input validation warnings."""
        self._logger.warning(f"Validation issue: {issue}")
    
    def log_history_limit_reached(self, max_size):
        """Log when history limit is reached."""
        self._logger.warning(f"History limit reached: {max_size} entries")
    
    def log_file_not_found(self, path):
        """Log when a file is not found."""
        self._logger.warning(f"File not found: {path}")
    
    # ERROR level methods
    def error(self, message, exc_info=False):
        """
        Log an error message.
        
        Args:
            message: Error message
            exc_info: Include exception traceback (default: False)
        """
        self._logger.error(message, exc_info=exc_info)
    
    def log_operation_error(self, operation, error_msg):
        """Log when an operation fails."""
        self._logger.error(f"Operation failed: {operation} - {error_msg}")
    
    def log_validation_error(self, value, reason):
        """Log input validation errors."""
        self._logger.error(f"Validation error for '{value}': {reason}")
    
    def log_division_by_zero(self, operand1, operation, operand2):
        """Log division by zero errors."""
        self._logger.error(
            f"Division by zero error: {operand1} {operation} {operand2}"
        )
    
    def log_invalid_operation(self, token):
        """Log when an invalid operation token is used."""
        self._logger.error(f"Invalid operation token: '{token}'")
    
    def log_file_error(self, path, error_msg):
        """Log file operation errors."""
        self._logger.error(f"File error with '{path}': {error_msg}")
    
    def log_data_error(self, operation, error_msg):
        """Log data-related errors."""
        self._logger.error(f"Data error during {operation}: {error_msg}")
    
    def log_config_error(self, error_msg):
        """Log configuration errors."""
        self._logger.error(f"Configuration error: {error_msg}")
    
    def log_exception(self, exception, context=""):
        """
        Log an exception with full traceback.
        
        Args:
            exception: The exception object
            context: Additional context about where/when it occurred
        """
        context_msg = f" ({context})" if context else ""
        self._logger.error(
            f"Exception occurred{context_msg}: {str(exception)}",
            exc_info=True
        )
    
    # DEBUG level methods
    def debug(self, message):
        """Log a debug message."""
        self._logger.debug(message)
    
    def log_input_received(self, operand1, operation, operand2):
        """Log when input is received."""
        self._logger.debug(
            f"Input received: {operand1} {operation} {operand2}"
        )
    
    def log_state_change(self, old_state, new_state):
        """Log state changes."""
        self._logger.debug(f"State changed: {old_state} -> {new_state}")
    
    @classmethod
    def get_instance(cls):
        """Get the singleton logger instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


# Convenience function to get logger instance
def get_logger():
    """Get the calculator logger instance."""
    return Logger.get_instance()
