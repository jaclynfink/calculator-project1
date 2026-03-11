from .calculator import Calculator
from .calculator_memento import HistoryMemento, HistoryCaretaker
from .history import History
from .exceptions import ValidationError, InvalidOperationError, OperationError, UndoRedoError
from .logger import get_logger
from colorama import Fore, Style, init

# Initialize colorama for cross-platform color support
init(autoreset=True)


class CalculatorREPL:
    """
    Interactive calculator using the REPL (Read-Eval-Print Loop) pattern.
    
    """
    
    def __init__(self, calculator=None):
        """
        Initialize the REPL.
        
        Args:
            calculator: Optional Calculator instance (creates new one if None)
        """
        self.calculator = calculator or Calculator()
        self.logger = get_logger()
        
        # Set up undo/redo system
        self._caretaker = HistoryCaretaker()
        # Save initial state
        self._save_state()
        
        # Map of command names to operation tokens
        self.operation_map = {
            'add': '+',
            'subtract': '-',
            'multiply': '*',
            'divide': '/',
            'power': 'pow',
            'root': 'root',
            'modulus': 'mod',
            'int_divide': '//',
            'percent': 'percent',
            'abs_diff': 'abs_diff'
        }
        
        self.logger.info("CalculatorREPL initialized")
    
    def _save_state(self):
        """Save current history state for undo/redo."""
        memento = HistoryMemento(self.calculator.history.df.copy(deep=True))
        self._caretaker.push(memento)
    
    def _parse_input(self, line):
        """
        Parse user input line.
        
        Args:
            line: User input string
            
        Returns:
            Tuple of (command, args) or (operation, operand1, operand2)
        """
        line = line.strip()
        
        if not line:
            return ('noop', [])
        
        parts = line.split()
        
        # Check if first part is a command
        first_word = parts[0].lower()
        if first_word in ['help', 'history', 'clear', 'undo', 'redo', 'save', 'load', 'exit', 'quit']:
            return (first_word, parts[1:])
        
        # Check if first part is an operation command
        if first_word in self.operation_map:
            if len(parts) >= 3:
                return ('calculate', [self.operation_map[first_word], parts[1], parts[2]])
            else:
                return ('error', ['Not enough operands for operation'])
        
        # Check for specific command format (e.g., 2 + 3)
        if len(parts) >= 3:
            operator = parts[1]
            if operator.lower() in self.operation_map:
                operator = self.operation_map[operator.lower()]
            return ('calculate', [operator, parts[0], parts[2]])
        
        return ('error', ['Invalid command. Type "help" for available commands.'])
    
    def _process_command(self, command, args):
        """
        Process a command.
        
        Args:
            command: Command name
            args: List of command arguments
            
        Returns:
            String response to display to user
        """
        try:
            if command == 'noop':
                return ''
            
            elif command in ['exit', 'quit']:
                return '__EXIT__'
            
            elif command == 'help':
                return self._help_text()
            
            elif command == 'history':
                return self._show_history()
            
            elif command == 'clear':
                self.calculator.history.clear()
                self._save_state()
                self.logger.info("History cleared")
                return f"{Fore.GREEN}History cleared.{Style.RESET_ALL}"
            
            elif command == 'undo':
                try:
                    memento = self._caretaker.undo()
                    self.calculator.history.df = memento.df.copy(deep=True)
                    self.logger.info("Undo performed")
                    return f"{Fore.GREEN}Undo successful.{Style.RESET_ALL}"
                except UndoRedoError as e:
                    return f"{Fore.YELLOW}Cannot undo: {e}{Style.RESET_ALL}"
            
            elif command == 'redo':
                try:
                    memento = self._caretaker.redo()
                    self.calculator.history.df = memento.df.copy(deep=True)
                    self.logger.info("Redo performed")
                    return f"{Fore.GREEN}Redo successful.{Style.RESET_ALL}"
                except UndoRedoError as e:
                    return f"{Fore.YELLOW}Cannot redo: {e}{Style.RESET_ALL}"
            
            elif command == 'save':
                path = args[0] if args else None
                self.calculator.history.save_csv(path)
                self.logger.log_history_saved(path or "default location")
                return f"History saved to {path or 'default location'}."
            
            elif command == 'load':
                path = args[0] if args else None
                self.calculator.history = History.load_csv(path)
                # Reset undo/redo after loading
                self._caretaker = HistoryCaretaker()
                self._save_state()
                self.logger.log_history_loaded(path or "default location", len(self.calculator.history.df))
                return f"History loaded from {path or 'default location'}."
            
            elif command == 'calculate':
                if len(args) < 3:
                    return "Error: Not enough arguments for calculation."
                
                operation_token, operand1, operand2 = args[0], args[1], args[2]
                
                try:
                    result = self.calculator.calculate(operand1, operation_token, operand2)
                    
                    # Save state for undo
                    self._save_state()
                    
                    return f"{Fore.GREEN}Result: {Fore.CYAN}{result}{Style.RESET_ALL}"
                
                except ZeroDivisionError:
                    return f"{Fore.RED}Error: Division by zero is not allowed.{Style.RESET_ALL}"
                except ValidationError as e:
                    return f"{Fore.RED}Validation Error: {e}{Style.RESET_ALL}"
                except InvalidOperationError as e:
                    return f"{Fore.RED}Invalid Operation: {e}{Style.RESET_ALL}"
                except OperationError as e:
                    return f"{Fore.RED}Operation Error: {e}{Style.RESET_ALL}"
            
            elif command == 'error':
                return f"{Fore.RED}Error: {args[0]}{Style.RESET_ALL}"
            
            else:
                return f"{Fore.RED}Unknown command: {command}. Type 'help' for available commands.{Style.RESET_ALL}"
        
        except Exception as e:
            self.logger.log_exception(e, context=f"processing command '{command}'")
            return f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}"
    
    def _show_history(self, n=10):
        """
        Get formatted history display.
        
        Args:
            n: Number of recent entries to show (default 10)
            
        Returns:
            Formatted history string
        """
        if self.calculator.history.is_empty():
            return f"{Fore.YELLOW}No calculation history available.{Style.RESET_ALL}"
        
        lines = [f"{Fore.CYAN}Calculation History (last {n} entries):{Style.RESET_ALL}"]
        lines.append(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
        
        recent = self.calculator.history.last(n)
        for idx, row in recent.iterrows():
            lines.append(f"{Fore.WHITE}{row['timestamp']} | {row['operand1']} {row['operation']} {row['operand2']} = {Fore.GREEN}{row['result']}{Style.RESET_ALL}")
        
        return "\n".join(lines)
    
    def _help_text(self):
        """
        Generate help text.
        
        Returns:
            Formatted help string
        """
        return """
Calculator REPL - Available Commands
=====================================

  add <a> <b>          Addition: a + b
  subtract <a> <b>     Subtraction: a - b
  multiply <a> <b>     Multiplication: a × b
  divide <a> <b>       Division: a ÷ b
  power <a> <b>        Power: a raised to power b
  root <a> <b>         Root: b-th root of a
  modulus <a> <b>      Modulus: a mod b
  int_divide <a> <b>   Integer division: a // b
  percent <a> <b>      Percentage: a% of b
  abs_diff <a> <b>     Absolute difference: |a - b|

  <a> + <b>            You can also use this notation
  <a> - <b>            Example: 5 + 3
  <a> * <b>            Example: 10 / 2

  history              Display calculation history
  clear                Clear all calculation history
  undo                 Undo last calculation
  redo                 Redo last undone calculation
  save [path]          Save history to CSV file
  load [path]          Load history from CSV file
  help                 Display this help message
  exit or quit         Exit the calculator

EXAMPLES:
  add 5 3              → Result: 8
  10 - 2               → Result: 8
  power 2 8            → Result: 256
  root 27 3            → Result: 3
  history              → Show recent calculations
"""
    
    def run(self): # pragma: no cover
        """Run the REPL loop."""
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}  Welcome to the Advanced Calculator!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Type {Fore.GREEN}'help'{Fore.WHITE} for available commands, {Fore.RED}'exit'{Fore.WHITE} to quit.{Style.RESET_ALL}")
        print()
        
        self.logger.info("REPL started")
        
        while True:
            try:
                user_input = input(f"{Fore.MAGENTA}calc> {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                # Parse input
                command, args = self._parse_input(user_input)
                
                # Process command
                output = self._process_command(command, args)
                
                # Check for exit
                if output == 'exit':
                    print(f"{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                    self.logger.info("REPL exited")
                    break
                
                # Print output
                if output:
                    print(output)
                    print()
            
            except KeyboardInterrupt:
                print(f"\n{Fore.YELLOW}Use 'exit' or 'quit' to exit the calculator.{Style.RESET_ALL}")
                print()
            except EOFError:
                print(f"\n{Fore.YELLOW}Goodbye!{Style.RESET_ALL}")
                self.logger.info("REPL exited (EOF)")
                break
            except Exception as e:
                self.logger.log_exception(e, context="REPL main loop")
                print(f"{Fore.RED}An unexpected error occurred: {e}{Style.RESET_ALL}")
                print()


def main():
    """Main entry point for the calculator REPL."""
    repl = CalculatorREPL()
    repl.run()


if __name__ == "__main__":
    main()
