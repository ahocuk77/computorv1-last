import os
import subprocess
import pytest

# Get the path to computor.py in the parent directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPUTOR_PATH = os.path.join(BASE_DIR, "computor.py")

def run_computor(equation, flag=None):
    cmd = ["python3", COMPUTOR_PATH, equation]
    if flag:
        cmd.append(flag)
        
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip() + result.stderr.strip()

# ==============================================================================
# BONUS TESTS: ERROR HANDLING, FREE-FORM ENTRY, FRACTIONS, VERBOSE
# ==============================================================================

def test_bonus_free_form_parsing():
    """BONUS: Test natural shorthand inputs (missing powers, disordered)."""
    output = run_computor("-x^2 + 4x - 3 + 12 - 2X^2 = -5 + X")
    assert "Reduced form: 14 * X^0 + 3 * X^1 - 3 * X^2 = 0" in output
    assert "Polynomial degree: 2" in output

@pytest.mark.parametrize("invalid_input, expected_error", [
    ("5X + 3Y = 0", "Invalid characters"),
    ("5X^2 + 4X^1.5 = 0", "whole numbers"),
    ("2 * X^-1 = 0", "cannot be negative"),
    ("5X++2=0", "consecutive operators"),
    ("= 5X", "empty side")
])
def test_bonus_syntax_lexical_errors(invalid_input, expected_error):
    """BONUS: Ensure the program catches errors and prints friendly messages instead of crashing."""
    output = run_computor(invalid_input)
    # The output should contain our custom error message
    assert expected_error in output
    
def test_bonus_fraction_output():
    """BONUS: Test irreducible fraction conversions."""
    output = run_computor("3X - 1 = 0")
    # Linear solution should be 0.333333 with (1/3) next to it
    assert "0.333333 (1/3)" in output

def test_bonus_verbose_mode():
    """BONUS: Test if the -v / --verbose flag prints intermediate steps."""
    output = run_computor("X^2 - 4 = 0", flag="--verbose")
    assert "[Verbose] Step 1:" in output
    assert "[Verbose] Calculating discriminant: Delta" in output

def test_bonus_help_menu():
    """BONUS: Test the usage/help menu."""
    output = run_computor("--help")
    assert "Usage:" in output
    assert "Options:" in output
    assert "Examples:" in output