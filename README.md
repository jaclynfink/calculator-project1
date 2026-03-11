## Project Description

Command-line calculator application that provides arithmetic operations and history management, logging, and error handling.

### Key Features
- **Arithmetic Operations**: Addition, subtraction, multiplication, division, power, root, modulus, integer division, percentage, and absolute difference
- **Interactive REPL Interface**: User-friendly command-line interface
- **History**: Save and load calculation history using pandas DataFrames saved as CSV
- **Undo/Redo**: Uses memento pattern implementation
- **Logging**: Detailed logging system for debugging
- **Input Validation**: Validation for safe calculations
- **Test Coverage**: Unit tests using pytest
- **CI/CD Integration**: Automated testing with GitHub Actions


## Installation Instructions

### Prerequisites
- Python 3.10 or higher
- pip (Python package installer)
- Git

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/jaclynfink/calculator-project1.git
   cd calculator-project1
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration Setup

### Creating the .env File

1. **Copy the example configuration file**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file with your preferred settings**


### Configuration Options Explained

- **CALCULATOR_LOG_DIR**: Specifies the directory where application logs will be stored. The directory is created automatically if it doesn't exist.
- **CALCULATOR_HISTORY_DIR**: Specifies the directory for saving calculation history CSV files. Created automatically on first save.
- **CALCULATOR_MAX_HISTORY_SIZE**: Limits the number of calculations kept in memory.
- **CALCULATOR_AUTO_SAVE**: When set to `true`, automatically saves history to CSV after each calculation.
- **CALCULATOR_PRECISION**: Controls the number of decimal places displayed in calculation results (default is 10 decimal places).
- **CALCULATOR_MAX_INPUT_VALUE**: Maximum allowed value for operands.
- **CALCULATOR_DEFAULT_ENCODING**: Character encoding for reading/writing CSV files (default: utf-8 for universal compatibility).


## Usage Guide

### Starting the Calculator

Run the interactive calculator REPL:
```bash
python -m app.calculation
```

You'll see the welcome screen:
```
============================================================
  Welcome to the Advanced Calculator!
============================================================
Type 'help' for available commands, 'exit' to quit.

calc>
```

### Command-Line Interface Commands

#### Calculation Commands

**Prefix Notation** (Operation first)
```
calc> + 5 3
Result: 8.0

calc> * 10 4
Result: 40.0
```

**Infix Notation** (Natural order)
```
calc> 5 + 3
Result: 8.0

calc> 10 * 4
Result: 40.0
```

#### Available Operations

| Operation | Symbols | Example | Result | Description |
|-----------|---------|---------|--------|-------------|
| **Addition** | `+`, `add` | `5 + 3` | 8.0 | Sum of two numbers |
| **Subtraction** | `-`, `subtract` | `10 - 4` | 6.0 | Difference between two numbers |
| **Multiplication** | `*`, `mul` | `6 * 7` | 42.0 | Product of two numbers |
| **Division** | `/`, `div` | `20 / 4` | 5.0 | Quotient (error on division by zero) |
| **Power** | `^`, `**`, `pow` | `2 ^ 8` | 256.0 | First number raised to second power |
| **Root** | `root`, `rt` | `27 root 3` | 3.0 | Nth root (cube root of 27 = 3) |
| **Modulus** | `%`, `mod` | `17 % 5` | 2.0 | Remainder of division |
| **Integer Division** | `//`, `intdiv` | `17 // 5` | 3.0 | Floor division result |
| **Percentage** | `percent`, `pct` | `25 percent 200` | 12.5 | What percent first is of second |
| **Absolute Difference** | `absdiff` | `15 absdiff 8` | 7.0 | Absolute value of difference |

#### System Commands

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Display help information and available commands | `help` |
| `history` | Show calculation history (last 10 entries) | `history` |
| `clear` | Clear all calculation history from memory | `clear` |
| `save [path]` | Save history to CSV file | `save` or `save myfile.csv` |
| `load [path]` | Load history from CSV file | `load` or `load myfile.csv` |
| `undo` | Undo last history change | `undo` |
| `redo` | Redo previously undone change | `redo` |
| `exit` | Exit the calculator application | `exit` |


## Testing Instructions

### Running Unit Tests

**Run all tests**
```bash
pytest
```

**Run specific test file**
```bash
pytest tests/test_calculator.py
```

**Run specific test function**
```bash
pytest tests/test_calculator.py::test_calculator_operations
```

### Checking Test Coverage

**Generate terminal coverage report**
```bash
pytest --cov=app --cov-report=term
```

**Generate detailed terminal report** (shows missing line numbers)
```bash
pytest --cov=app --cov-report=term-missing
```

**Generate HTML coverage report** (interactive browser view)
```bash
pytest --cov=app --cov-report=html
```
Then open `htmlcov/index.html` in your web browser to view detailed coverage analysis.

**Enforce minimum coverage threshold**
```bash
pytest --cov=app --cov-fail-under=90
```
This command will fail if coverage drops below 90%.


## CI/CD Information

### GitHub Actions Workflow

**File Location**: `.github/workflows/python-app.yml`

**Triggers**:
- Automatically runs on push to `main` branch
- Automatically runs on pull requests to `main` branch

### Pipeline Steps

The CI/CD pipeline executes the following steps:

1. **Check out code**: Clones the repository using `actions/checkout@v3`
2. **Set up Python environment**: Installs Python 3.10 using `actions/setup-python@v4`
3. **Install dependencies**: Installs all packages from `requirements.txt` including pytest and pytest-cov
4. **Run tests with coverage**: Executes `pytest --cov=app --cov-fail-under=90`
5. **Enforce coverage threshold**: Pipeline fails if test coverage drops below 90%