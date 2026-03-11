"""
Tests for the Calculator REPL.
"""

import pytest
from app.calculation import CalculatorREPL
from app.calculator import Calculator
from app.history import History


class TestCalculatorREPL:
    """Test the REPL interface."""
    
    def test_repl_initialization(self):
        """Test REPL initializes correctly."""
        repl = CalculatorREPL()
        assert repl.calculator is not None
        assert repl.logger is not None
        assert repl._caretaker is not None
    
    def test_parse_input_command(self):
        """Test parsing simple commands."""
        repl = CalculatorREPL()
        
        command, args = repl._parse_input("help")
        assert command == "help"
        assert args == []
        
        command, args = repl._parse_input("history")
        assert command == "history"
        assert args == []
        
        command, args = repl._parse_input("exit")
        assert command == "exit"
        assert args == []
    
    def test_parse_input_operation_prefix(self):
        """Test parsing operations in prefix notation."""
        repl = CalculatorREPL()
        
        command, args = repl._parse_input("add 5 3")
        assert command == "calculate"
        assert args == ['+', '5', '3']
        
        command, args = repl._parse_input("multiply 4 2")
        assert command == "calculate"
        assert args == ['*', '4', '2']
        
        command, args = repl._parse_input("power 2 8")
        assert command == "calculate"
        assert args == ['pow', '2', '8']
    
    def test_parse_input_operation_infix(self):
        """Test parsing operations in infix notation."""
        repl = CalculatorREPL()
        
        command, args = repl._parse_input("5 + 3")
        assert command == "calculate"
        assert args == ['+', '5', '3']
        
        command, args = repl._parse_input("10 - 2")
        assert command == "calculate"
        assert args == ['-', '10', '2']
        
        command, args = repl._parse_input("4 * 3")
        assert command == "calculate"
        assert args == ['*', '4', '3']
    
    def test_parse_input_empty(self):
        """Test parsing empty input."""
        repl = CalculatorREPL()
        
        command, args = repl._parse_input("")
        assert command == "noop"
        assert args == []
        
        command, args = repl._parse_input("   ")
        assert command == "noop"
        assert args == []
    
    def test_process_command_help(self):
        """Test help command processing."""
        repl = CalculatorREPL()
        result = repl._process_command("help", [])
        assert "Calculator REPL - Available Commands" in result
        assert "add" in result
        assert "subtract" in result
        assert "EXAMPLES" in result
    
    def test_process_command_exit(self):
        """Test exit command processing."""
        repl = CalculatorREPL()
        result = repl._process_command("exit", [])
        assert result == "__EXIT__"
        
        result = repl._process_command("quit", [])
        assert result == "__EXIT__"
    
    def test_process_command_calculate_add(self):
        """Test calculation command - addition."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['+', '5', '3'])
        assert "Result: 8" in result
    
    def test_process_command_calculate_subtract(self):
        """Test calculation command - subtraction."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['-', '10', '2'])
        assert "Result: 8" in result
    
    def test_process_command_calculate_multiply(self):
        """Test calculation command - multiplication."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['*', '4', '2'])
        assert "Result: 8" in result
    
    def test_process_command_calculate_divide(self):
        """Test calculation command - division."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['/', '16', '2'])
        assert "Result: 8" in result
    
    def test_process_command_calculate_power(self):
        """Test calculation command - power."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['pow', '2', '3'])
        assert "Result: 8" in result
    
    def test_process_command_calculate_root(self):
        """Test calculation command - root."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['root', '27', '3'])
        assert "Result: 3" in result
    
    def test_process_command_calculate_modulus(self):
        """Test calculation command - modulus."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['mod', '10', '3'])
        assert "Result: 1" in result
    
    def test_process_command_calculate_int_divide(self):
        """Test calculation command - integer division."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['//', '17', '5'])
        assert "Result: 3" in result
    
    def test_process_command_calculate_percent(self):
        """Test calculation command - percentage."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['percent', '20', '50'])
        assert "Result: 40" in result 
    
    def test_process_command_calculate_abs_diff(self):
        """Test calculation command - absolute difference."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['abs_diff', '5', '12'])
        assert "Result: 7" in result
    
    def test_process_command_history_empty(self):
        """Test history command with empty history."""
        repl = CalculatorREPL()
        result = repl._process_command("history", [])
        assert "No calculation history" in result
    
    def test_process_command_history_with_data(self):
        """Test history command with calculations."""
        repl = CalculatorREPL()
        repl._process_command("calculate", ['+', '5', '3'])
        repl._process_command("calculate", ['-', '10', '2'])
        
        result = repl._process_command("history", [])
        assert "Calculation History" in result
        assert "5.0 + 3.0 = 8" in result
        assert "10.0 - 2.0 = 8" in result
    
    def test_process_command_clear(self):
        """Test clear command."""
        repl = CalculatorREPL()
        repl._process_command("calculate", ['+', '5', '3'])
        assert not repl.calculator.history.is_empty()
        
        result = repl._process_command("clear", [])
        assert "History cleared" in result
        assert repl.calculator.history.is_empty()
    
    def test_process_command_undo(self):
        """Test undo command."""
        repl = CalculatorREPL()
        
        # Perform calculations
        repl._process_command("calculate", ['+', '5', '3'])
        repl._process_command("calculate", ['-', '10', '2'])
        
        # Should have 2 entries
        assert len(repl.calculator.history.df) == 2
        
        # Undo once
        result = repl._process_command("undo", [])
        assert "Undo successful" in result
        assert len(repl.calculator.history.df) == 1
        
        # Undo again
        result = repl._process_command("undo", [])
        assert "Undo successful" in result
        assert len(repl.calculator.history.df) == 0
    
    def test_process_command_redo(self):
        """Test redo command."""
        repl = CalculatorREPL()
        
        # Perform calculation
        repl._process_command("calculate", ['+', '5', '3'])
        assert len(repl.calculator.history.df) == 1
        
        # Undo
        repl._process_command("undo", [])
        assert len(repl.calculator.history.df) == 0
        
        # Redo
        result = repl._process_command("redo", [])
        assert "Redo successful" in result
        assert len(repl.calculator.history.df) == 1
    
    def test_process_command_undo_at_start(self):
        """Test undo when at the beginning."""
        repl = CalculatorREPL()
        result = repl._process_command("undo", [])
        assert "Cannot undo" in result
    
    def test_process_command_redo_at_end(self):
        """Test redo when at the end."""
        repl = CalculatorREPL()
        repl._process_command("calculate", ['+', '5', '3'])
        result = repl._process_command("redo", [])
        assert "Cannot redo" in result
    
    def test_process_command_save_load(self, tmp_path):
        """Test save and load commands."""
        repl = CalculatorREPL()
        
        # Perform some calculations
        repl._process_command("calculate", ['+', '5', '3'])
        repl._process_command("calculate", ['*', '4', '2'])
        
        # Save to file
        save_path = str(tmp_path / "test_history.csv")
        result = repl._process_command("save", [save_path])
        assert "History saved" in result
        
        # Clear history
        repl._process_command("clear", [])
        assert repl.calculator.history.is_empty()
        
        # Load from file
        result = repl._process_command("load", [save_path])
        assert "History loaded" in result
        assert len(repl.calculator.history.df) == 2
    
    def test_process_command_division_by_zero(self):
        """Test division by zero error handling."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['/', '10', '0'])
        assert "Division by zero" in result
    
    def test_process_command_invalid_number(self):
        """Test invalid number error handling."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['+', 'abc', '3'])
        assert "Validation Error" in result or "Error" in result
    
    def test_operation_map_completeness(self):
        """Test that all required operations are in the map."""
        repl = CalculatorREPL()
        
        required_operations = [
            'add', 'subtract', 'multiply', 'divide', 
            'power', 'root', 'modulus', 'int_divide', 
            'percent', 'abs_diff'
        ]
        
        for op in required_operations:
            assert op in repl.operation_map, f"Operation '{op}' not in operation_map"
    
    def test_help_text_contains_all_commands(self):
        """Test that help text includes all required commands."""
        repl = CalculatorREPL()
        help_text = repl._help_text()
        
        required_in_help = [
            'add', 'subtract', 'multiply', 'divide',
            'power', 'root', 'modulus', 'int_divide',
            'percent', 'abs_diff', 'history', 'clear',
            'undo', 'redo', 'save', 'load', 'help', 'exit'
        ]
        
        for cmd in required_in_help:
            assert cmd in help_text.lower(), f"Command '{cmd}' not in help text"
    
    def test_parse_input_insufficient_operands(self):
        """Test parsing operation with insufficient operands."""
        repl = CalculatorREPL()
        
        command, args = repl._parse_input("add 5")
        assert command == "error"
        assert "Not enough operands" in args[0]
    
    def test_parse_input_infix_with_command_name(self):
        """Test parsing infix notation with command name as operator."""
        repl = CalculatorREPL()
        
        command, args = repl._parse_input("5 add 3")
        assert command == "calculate"
        assert args == ['+', '5', '3']
    
    def test_parse_input_invalid_format(self):
        """Test parsing invalid input format."""
        repl = CalculatorREPL()
        
        command, args = repl._parse_input("random text")
        assert command == "error"
        assert "Invalid command" in args[0]
    
    def test_process_command_calculate_insufficient_args(self):
        """Test calculate command with insufficient arguments."""
        repl = CalculatorREPL()
        result = repl._process_command("calculate", ['+', '5'])
        assert "Not enough arguments" in result
    
    def test_process_command_unknown_command(self):
        """Test processing unknown command."""
        repl = CalculatorREPL()
        result = repl._process_command("unknown", [])
        assert "Unknown command" in result
    
    def test_process_command_error_type(self):
        """Test processing error command type."""
        repl = CalculatorREPL()
        result = repl._process_command("error", ["Test error message"])
        assert "Error: Test error message" in result
    
    def test_process_command_exception_handling(self):
        """Test exception handling in process_command."""
        repl = CalculatorREPL()
        # Force an exception by passing invalid data
        result = repl._process_command("calculate", ['+', '5', '3', 'extra'])
        # Should still return a result without crashing
        assert "Result:" in result or "Error" in result
    
    def test_show_history_formatting(self):
        """Test history display formatting."""
        repl = CalculatorREPL()
        repl._process_command("calculate", ['+', '5', '3'])
        
        history_output = repl._show_history(n=10)
        assert "Calculation History" in history_output
        assert "5.0 + 3.0 = 8" in history_output
    
    def test_save_default_path(self, tmp_path):
        """Test save with explicit path."""
        repl = CalculatorREPL()
        repl._process_command("calculate", ['+', '5', '3'])
        save_path = str(tmp_path / "test.csv")
        result = repl._process_command("save", [save_path])
        assert "History saved" in result
    
    def test_load_default_path(self, tmp_path):
        """Test load with explicit path."""
        repl = CalculatorREPL()
        # First save something
        repl._process_command("calculate", ['+', '5', '3'])
        save_path = str(tmp_path / "test.csv")
        repl._process_command("save", [save_path])
        # Then load it
        result = repl._process_command("load", [save_path])
        assert "History loaded" in result
