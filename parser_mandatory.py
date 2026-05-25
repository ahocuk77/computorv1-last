import re

def clean_and_tokenize(equation_str: str) -> str:
    """MANDATORY: Basic whitespace cleaning and valid character check."""
    cleaned = re.sub(r'\s+', '', equation_str)
    
    if not re.match(r'^[0-9X.+\-*^=]+$', cleaned):
        raise ValueError("Strict Error: Invalid characters detected.")
        
    if cleaned.count('=') != 1:
        raise ValueError("Strict Error: The equation must contain exactly one '=' sign.")
        
    return cleaned


def parse_term(term_str: str) -> tuple[float, int]:
    """
    MANDATORY: Only accepts the 'a * X^p' format.
    Rejects any implicit coefficients or exponents (e.g., '5', 'X^2').
    """
    if "*X^" not in term_str:
        raise ValueError(
            f"Strict Format Violation in term '{term_str}'. "
            "All terms must be strictly formatted as 'a * X^p' (e.g., 5 * X^0)."
        )

    parts = term_str.split('*X^')
    coeff_part = parts[0]
    exp_part = parts[1]

    try:
        coefficient = float(coeff_part)
    except ValueError:
        raise ValueError(f"Strict Error: Invalid coefficient in term '{term_str}'")

    try:
        exponent = int(exp_part)
        if exponent < 0:
            raise ValueError("Strict Error: Polynomial exponents cannot be negative.")
    except ValueError:
        raise ValueError(f"Strict Error: Invalid exponent in term '{term_str}'")

    return coefficient, exponent


def parse_equation(equation_str: str) -> dict[int, float]:
    """MANDATORY: Splits the equation by the equality sign and generates a coefficients dictionary."""
    cleaned = clean_and_tokenize(equation_str)
    coefficients = {0: 0.0, 1: 0.0, 2: 0.0}
    
    lhs_str, rhs_str = cleaned.split('=')
    
    lhs_terms = [t for t in re.split(r'(?=[+-])', lhs_str) if t]
    rhs_terms = [t for t in re.split(r'(?=[+-])', rhs_str) if t]

    for term in lhs_terms:
        coeff, exp = parse_term(term)
        coefficients[exp] = coefficients.get(exp, 0.0) + coeff

    for term in rhs_terms:
        coeff, exp = parse_term(term)
        coefficients[exp] = coefficients.get(exp, 0.0) - coeff

    return coefficients