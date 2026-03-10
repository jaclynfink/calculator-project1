import os
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
    
    def __init__(self, history_file, autosave, strategy):
        """    
        history_file: Path to history CSV file, which has the history of calculations
        autosave: True to auto-save, False otherwise
        strategy: "EAFP" or "LBYL"
        """
        self.history_file = history_file
        self.autosave = autosave
        self.strategy = strategy
    
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
        
        # Get history file path (default: calculator_history.csv)
        history_file = os.getenv("CALC_HISTORY_FILE", "calculator_history.csv").strip()
        if not history_file:
            raise ConfigError("CALC_HISTORY_FILE cannot be empty")
        
        # Get autosave setting (default: True)
        autosave_text = os.getenv("CALC_AUTOSAVE", "1")
        autosave = parse_boolean(autosave_text)
        
        # Get strategy (default: EAFP)
        strategy = os.getenv("CALC_STRATEGY", "EAFP").strip().upper()
        if strategy not in {"EAFP", "LBYL"}:
            raise ConfigError("ERROR: CALC_STRATEGY must be either 'EAFP' or 'LBYL'")
        
        # Create and return the config object
        return cls(
            history_file=history_file,
            autosave=autosave,
            strategy=strategy,
        )