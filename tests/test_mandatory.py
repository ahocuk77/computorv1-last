import os
import subprocess
import pytest

# Get the path to computor.py in the parent directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPUTOR_PATH = os.path.join(BASE_DIR, "computor.py")

def run_computor(equation):
    result = subprocess.run(
        ["python3", COMPUTOR_PATH, equation], 
        capture_output=True, 
        text=True
    )
    return result.stdout.strip() + result.stderr.strip()

# ==============================================================================
# MANDATORY TESTS: STRICT SUBJECT COMPLIANCE
# ==============================================================================

def test_pdf_example_1():
    output = run_computor("5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
    assert "Reduced form: 4 * X^0 + 4 * X^1 - 9.3 * X^2 = 0" in output
    assert "Polynomial degree: 2" in output
    assert "Discriminant is strictly positive" in output
    assert "0.905239" in output
    assert "-0.475131" in output

def test_pdf_example_2():
    output = run_computor("5 * X^0 + 4 * X^1 = 4 * X^0")
    assert "Reduced form: 1 * X^0 + 4 * X^1 = 0" in output
    assert "Polynomial degree: 1" in output
    assert "The solution is:" in output
    assert "-0.25" in output

def test_pdf_example_3():
    output = run_computor("8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0")
    assert "Reduced form: 5 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 0" in output
    assert "Polynomial degree: 3" in output
    assert "strictly greater than 2, I can't solve" in output

def test_pdf_example_4():
    output = run_computor("6 * X^0 = 6 * X^0")
    assert "Reduced form: 0 * X^0 = 0" in output
    assert "Polynomial degree: 0" in output
    assert "Any real number is a solution" in output

def test_no_solution_contradiction():
    output = run_computor("10 * X^0 = 15 * X^0")
    assert "Reduced form: -5 * X^0 = 0" in output
    assert "Polynomial degree: 0" in output
    assert "No solution" in output

def test_complex_roots():
    output = run_computor("1 * X^0 + 2 * X^1 + 5 * X^2 = 0 * X^0")
    assert "Reduced form: 1 * X^0 + 2 * X^1 + 5 * X^2 = 0" in output
    assert "Polynomial degree: 2" in output
    assert "Discriminant is strictly negative" in output
    assert "-0.2 + 0.4i" in output
    assert "-0.2 - 0.4i" in output