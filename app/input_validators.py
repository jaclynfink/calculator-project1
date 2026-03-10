"""
Input validation module for calculator operations.
Validates user inputs to ensure they are numerical and within allowed ranges.
"""

from .exceptions import ValidationError
from .calculator_config import CalculatorConfig


class InputValidator:
    """Validates calculator inputs against configured rules."""
    
    def __init__(self, config=None):
        """
        Initialize validator with configuration.
        
        Args:
            config: CalculatorConfig object with validation rules
        """
        self.config = config or CalculatorConfig.load()
    
    def validate_number(self, value, parameter_name="input"):
        """
        Validate that a value is a valid number within allowed range.
        
        Args:
            value: The value to validate
            parameter_name: Name of the parameter (for error messages)
            
        Returns:
            float: The validated number
            
        Raises:
            ValidationError: If validation fails
        """
        # Check if it's a number
        if not isinstance(value, (int, float)):
            try:
                value = float(value)
            except (ValueError, TypeError):
                raise ValidationError(
                    f"Invalid {parameter_name}: '{value}' is not a valid number. "
                    f"Please provide a numerical value."
                )
        
        # Check for special float values
        if not self._is_finite(value):
            raise ValidationError(
                f"Invalid {parameter_name}: '{value}' is not a finite number. "
                f"Please provide a valid numerical value (not infinity or NaN)."
            )
        
        # Check range
        if abs(value) > self.config.max_input_value:
            raise ValidationError(
                f"Invalid {parameter_name}: '{value}' exceeds maximum allowed value. "
                f"Please provide a number between -{self.config.max_input_value} and {self.config.max_input_value}."
            )
        
        return float(value)
    
    def validate_operands(self, a, b):
        """
        Validate both operands for a calculation.
        
        Args:
            a: First operand
            b: Second operand
            
        Returns:
            tuple: (validated_a, validated_b)
            
        Raises:
            ValidationError: If validation fails
        """
        validated_a = self.validate_number(a, "first operand")
        validated_b = self.validate_number(b, "second operand")
        
        return validated_a, validated_b
    
    def validate_operation_token(self, token):
        """
        Validate that an operation token is not empty.
        
        Args:
            token: The operation token to validate
            
        Returns:
            str: The validated token
            
        Raises:
            ValidationError: If token is invalid
        """
        if not token or not isinstance(token, str):
            raise ValidationError(
                "Invalid operation: Operation token cannot be empty. "
                "Please provide a valid operation (e.g., '+', '-', '*', '/')."
            )
        
        return token.strip()
    
    def _is_finite(self, value):
        """
        Check if a value is a finite number (not infinity or NaN).
        
        Args:
            value: The value to check
            
        Returns:
            bool: True if finite, False otherwise
        """
        import math
        return math.isfinite(value)
    
    def round_result(self, result):
        """
        Round a result to the configured precision.
        
        Args:
            result: The result to round
            
        Returns:
            float: The rounded result
        """
        if self.config.precision >= 0:
            return round(result, self.config.precision)
        return result
