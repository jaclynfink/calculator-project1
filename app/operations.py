from abc import ABC, abstractmethod

from app.exceptions import InvalidOperationError

class Operation(ABC):
    """
    Class for all arithmetic operations.
    
    Each operation has:
    - token: what the user types
    - symbol: what gets displayed
    - execute(): method that does the calculation
    """
    
    token = ""  
    symbol = "" 
    
    @abstractmethod
    def execute(self, a, b):
        """
        Do the math operation. Must be implemented by each operation class.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Result of the operation
        """
        raise NotImplementedError("ERROR: Subclasses must implement execute()")  # pragma: no cover


class Add(Operation):
    token = "+"
    symbol = "+"
    
    def execute(self, a, b):
        return a + b


class Subtract(Operation):
    token = "-"
    symbol = "-"
    
    def execute(self, a, b):
        return a - b


class Multiply(Operation):
    token = "*"
    symbol = "*"
    
    def execute(self, a, b):
        return a * b


class Divide(Operation):
    token = "/"
    symbol = "/"
    
    def execute(self, a, b):
        """Return a / b, but check for division by zero first."""
        if b == 0:
            raise ZeroDivisionError("ERROR: cannot divide by zero")
        return a / b


class Power(Operation):
    token = "pow"
    symbol = "^"
    
    def execute(self, a, b):
        return a ** b


class Root(Operation):
    token = "root"
    symbol = "root"
    
    def execute(self, a, b):
        """
        Calculate the bth root of a.
        """
        # Check for root of 0
        if b == 0:
            raise ZeroDivisionError("ERROR: cannot take zeroth root")
        
        # Check for even root of negative number
        if a < 0 and float(b).is_integer() and int(b) % 2 == 0:
            raise ValueError("ERROR: even root of negative number")
        
        return a ** (1.0 / b)
    
class Modulus(Operation):
    token = "mod"
    symbol = "%"

    def execute(self, a, b):
        if b == 0:
            raise ZeroDivisionError("ERROR: cannot take modulus by zero")
        return a % b

class IntegerDivision(Operation):
    token = "intdiv"
    symbol = "//" 
    def execute(self, a, b):
        if b == 0:
            raise ZeroDivisionError("ERROR: cannot take integer division by zero")
        return a // b

class Percentage(Operation):
    token = "percent"
    symbol = "percent"

    def execute(self, a, b):
        # Calculate what percentage a is of b: (a / b) * 100
        if b == 0:
            raise ZeroDivisionError("ERROR: cannot calculate percentage with zero as denominator")
        return (a / b) * 100
    
class AbsoluteDifference(Operation):
    token = "absdiff"
    symbol = "abs_diff"

    def execute(self, a, b):
        return abs(a - b)


class OperationFactory:
    """
    Factory pattern to create operation objects based on user input.
    """
    
    _operation_map = {
        "+": Add,
        "add": Add,
        
        "-": Subtract,
        "sub": Subtract,
        "subtract": Subtract,
        
        "*": Multiply,
        "mul": Multiply,
        "multiply": Multiply,
        
        "/": Divide,
        "div": Divide,
        "divide": Divide,
        
        "^": Power,
        "**": Power,
        "pow": Power,
        "power": Power,
        
        "root": Root,
        "rt": Root,

        "mod": Modulus,
        "modulus": Modulus,
        "%": Modulus,

        "intdiv": IntegerDivision,
        "//": IntegerDivision,

        "percent": Percentage,
        "pct": Percentage,
        "percentage": Percentage,

        "abs_diff": AbsoluteDifference,
        "absdiff": AbsoluteDifference
    }
    
    @classmethod
    def create(cls, token):
        """
        Create an operation object based on user input.
        
        Args:
            token: What the user typed
            
        Returns:
            An operation object
            
        """
        token_clean = token.strip().lower()
        
        if token_clean in cls._operation_map:
            operation_class = cls._operation_map[token_clean]
            return operation_class()
        else:
            raise InvalidOperationError("ERROR Invalid operation. Type 'help' for valid operations.")