import re

def clean_and_tokenize(equation_str: str) -> str:
    """
    [BONUS: Syntax and Lexical Error Handling]
    Instead of assuming perfect input, this function validates the equation.
    Cleans all forms of whitespaces (\t, \n, spaces) and strictly validates 
    both lexical correctness and syntax boundaries. Raises ValueError on any violation.
    """
    # Remove ALL types of whitespace characters
    cleaned = re.sub(r'\s+', '', equation_str)
    
    # Lexical check - Only allow strict polynomial characters
    if not re.match(r'^[0-9xX.+\-*^=]+$', cleaned):
        raise ValueError("Invalid characters detected in the equation.")
        
    # Syntax check - Validate equality structure
    if cleaned.count('=') != 1:
        raise ValueError("The equation must contain exactly one '=' sign.")
        
    # Syntax check - Block completely empty sides around '='
    if cleaned.startswith('=') or cleaned.endswith('='):
        raise ValueError("The equation cannot have an empty side around '='.")
        
    # Syntax check - Block invalid consecutive operators (e.g., ++, +-, *+, ^*, ==)
    # Allows a minus sign after '=' or after another operator for negative terms
    if re.search(r'[+*^=]{2,}', cleaned) or re.search(r'\+-[+\-*^=]', cleaned) or re.search(r'-\+[+\-*^=]', cleaned):
        raise ValueError("Invalid consecutive operators detected.")
    if re.search(r'\*\*|\^\^|\+\+|\-\-', cleaned):
        raise ValueError("Invalid duplicated operators detected.")
        
    # Mathematical boundary - Block float exponents (e.g., X^1.5)
    if re.search(r'\^[0-9]+\.[0-9]+', cleaned):
        raise ValueError("Polynomial exponents must be whole numbers.")

    # Mathematical boundary - Block negative exponents (e.g., X^-1)
    if re.search(r'\^\-', cleaned):
        raise ValueError("Polynomial exponents cannot be negative.")
        
    return cleaned


def parse_term(term_str: str) -> tuple[float, int]:
    """
    [BONUS: Free-Form Entry & Bulletproof Parsing]
    Parses flexible terms like '4X^2', '-X', '+5', '4.2X', or 'X'.
    Includes strict mathematical boundary checks to prevent native crashes.
    """
    term_str = term_str.replace('x', 'X')
    

    if term_str.count('X') > 1:
        raise ValueError(f"Invalid term format: '{term_str}'. Multiple 'X's are not allowed.")
        

    if 'X' not in term_str:
        try:
            return float(term_str), 0
        except ValueError:
            raise ValueError(f"Invalid numeric constant: '{term_str}'")

    parts = term_str.split('X')
    coeff_part = parts[0]
    exp_part = parts[1]


    if coeff_part == "" or coeff_part == "+":
        coefficient = 1.0
    elif coeff_part == "-":
        coefficient = -1.0
    else:
        if coeff_part.endswith('*'):
            coeff_part = coeff_part[:-1]

        if coeff_part in ("", "+", "-"):
            raise ValueError(f"Invalid coefficient syntax in term: '{term_str}'")
            
        try:
            coefficient = float(coeff_part)
        except ValueError:
            raise ValueError(f"Could not parse coefficient in term: '{term_str}'")

    if exp_part == "":
        exponent = 1
    else:
        if exp_part.startswith('^'):
            exp_part = exp_part[1:]
        try:
            exponent = int(exp_part)
        except ValueError:
            raise ValueError(f"Invalid exponent in term: '{term_str}'")

    return coefficient, exponent


def parse_equation(equation_str: str) -> dict[int, float]:
    """
    [BONUS: Free-Form Entry]
    Advanced parser supporting fully free-form entries.
    Handles unsorted terms, dynamically groups them by degree, and 
    mathematically moves all right-hand side terms to the left-hand side.
    """
    cleaned = clean_and_tokenize(equation_str)
    coefficients = {0: 0.0, 1: 0.0, 2: 0.0}
    
    lhs_str, rhs_str = cleaned.split('=')
    
    # Split terms using lookahead regex before '+' or '-' to preserve signs
    lhs_terms = [t for t in re.split(r'(?=[+-])', lhs_str) if t]
    rhs_terms = [t for t in re.split(r'(?=[+-])', rhs_str) if t]

    # Add left-hand side terms to the dictionary
    for term in lhs_terms:
        coeff, exp = parse_term(term)
        coefficients[exp] = coefficients.get(exp, 0.0) + coeff

    # Subtract right-hand side terms to simulate moving them to the left
    for term in rhs_terms:
        coeff, exp = parse_term(term)
        coefficients[exp] = coefficients.get(exp, 0.0) - coeff

    return coefficients