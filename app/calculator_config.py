import os
from pathlib import Path
from dotenv import load_dotenv
from .exceptions import ConfigError


def parse_boolean(value):
    """
    Convert a string to a boolean value.
    
    Valid inputs: "true", "yes", "1", "on" = True
                  "false", "no", "0", "off" = False
    
    Args:
        value: String to convert to boolean
        
    Returns:
        Boolean
        
    Raises:
        ConfigError: If value is not a valid boolean string
    """
    value_lower = value.strip().lower()
    
    if value_lower in {"1", "true", "yes", "y", "on"}:
        return True
    
    if value_lower in {"0", "false", "no", "n", "off"}:
        return False
    
    raise ConfigError(f"Invalid boolean value: {value}")


class CalculatorConfig:
    
    def __init__(
        self, 
        log_dir,
        history_dir,
        max_history_size,
        auto_save,
        precision,
        max_input_value,
        default_encoding
    ):
        """
        Calculator configuration settings.
        
        Args:
            log_dir: Directory for log files
            history_dir: Directory for history files
            max_history_size: Maximum number of history entries
            auto_save: Whether to auto-save history
            precision: Number of decimal places for calculations
            max_input_value: Maximum allowed input value
            default_encoding: Default encoding for file operations
        """
        self.log_dir = Path(log_dir)
        self.history_dir = Path(history_dir)
        self.max_history_size = max_history_size
        self.auto_save = auto_save
        self.precision = precision
        self.max_input_value = max_input_value
        self.default_encoding = default_encoding
        
        # Legacy properties for backward compatibility
        self.history_file = str(self.history_dir / "calculator_history.csv")
        self.autosave = auto_save
    
    @classmethod
    def load(cls):
        """
        Load configuration from environment variables and .env file.
        
        Reads .env file if it exists, then reads environment variables.
        Environment variables override .env file.
        
        Returns:
            A CalculatorConfig object with loaded settings
            
        Raises:
            ConfigError: If settings are invalid
        """
        # Load settings from .env file (if it exists)
        load_dotenv(override=False)
        
        # === Base Directories ===
        log_dir = os.getenv("CALCULATOR_LOG_DIR", "logs").strip()
        if not log_dir:
            raise ConfigError("CALCULATOR_LOG_DIR cannot be empty")
        
        history_dir = os.getenv("CALCULATOR_HISTORY_DIR", "history").strip()
        if not history_dir:
            raise ConfigError("CALCULATOR_HISTORY_DIR cannot be empty")
        
        # Create directories if they don't exist
        Path(log_dir).mkdir(parents=True, exist_ok=True)
        Path(history_dir).mkdir(parents=True, exist_ok=True)
        
        # === History Settings ===
        max_history_size_str = os.getenv("CALCULATOR_MAX_HISTORY_SIZE", "1000").strip()
        try:
            max_history_size = int(max_history_size_str)
            if max_history_size <= 0:
                raise ConfigError("CALCULATOR_MAX_HISTORY_SIZE must be positive")
        except ValueError:
            raise ConfigError(f"CALCULATOR_MAX_HISTORY_SIZE must be an integer, got: {max_history_size_str}")
        
        auto_save_text = os.getenv("CALCULATOR_AUTO_SAVE", "true").strip()
        auto_save = parse_boolean(auto_save_text)
        
        # === Calculation Settings ===
        precision_str = os.getenv("CALCULATOR_PRECISION", "10").strip()
        try:
            precision = int(precision_str)
            if precision < 0:
                raise ConfigError("CALCULATOR_PRECISION must be non-negative")
        except ValueError:
            raise ConfigError(f"CALCULATOR_PRECISION must be an integer, got: {precision_str}")
        
        max_input_value_str = os.getenv("CALCULATOR_MAX_INPUT_VALUE", "1000000").strip()
        try:
            max_input_value = float(max_input_value_str)
            if max_input_value <= 0:
                raise ConfigError("CALCULATOR_MAX_INPUT_VALUE must be positive")
        except ValueError:
            raise ConfigError(f"CALCULATOR_MAX_INPUT_VALUE must be a number, got: {max_input_value_str}")
        
        default_encoding = os.getenv("CALCULATOR_DEFAULT_ENCODING", "utf-8").strip()
        if not default_encoding:
            raise ConfigError("CALCULATOR_DEFAULT_ENCODING cannot be empty")
        
        # Create and return the config object
        return cls(
            log_dir=log_dir,
            history_dir=history_dir,
            max_history_size=max_history_size,
            auto_save=auto_save,
            precision=precision,
            max_input_value=max_input_value,
            default_encoding=default_encoding
        )