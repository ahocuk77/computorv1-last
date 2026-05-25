from math_custom import custom_sqrt, absolute_value

def custom_gcd(a: int, b: int) -> int:
    """Calculates the Greatest Common Divisor using the Euclidean algorithm."""
    while b:
        a, b = b, a % b
    return absolute_value(a)

def to_fraction(val: float, limit: int = 100) -> tuple[int, int] | None:
    """Attempts to convert a float to an irreducible fraction tuple (numerator, denominator)."""
    val_abs = absolute_value(val)
    for den in range(1, limit):
        num = round(val_abs * den)
        if absolute_value(val_abs - (num / den)) < 1e-6:
            gcd = custom_gcd(int(num), int(den))
            return int(num // gcd), int(den // gcd)
    return None

def format_fraction_bonus(value: float) -> str:
    """Bonus: Appends irreducible fraction to real number solutions."""
    if value.is_integer():
        return ""
    fraction = to_fraction(value, limit=20)
    if fraction:
        num, den = fraction
        sign = "-" if value < 0 else ""
        return f" ({sign}{num}/{den})"
    return ""

def format_complex_part(value: float, is_imaginary: bool = False) -> str:
    """Formats complex numbers exactly like the PDF example (fractions where possible)."""
    val_abs = absolute_value(value)
    if val_abs.is_integer():
        res = str(int(val_abs))
        return f"{res}i" if is_imaginary else ("-" + res if value < 0 else res)
        
    fraction = to_fraction(val_abs, limit=100)
    if fraction:
        num, den = fraction
        return f"{num}i/{den}" if is_imaginary else ("-" + f"{num}/{den}" if value < 0 else f"{num}/{den}")
        
    res = f"{val_abs:.6f}".rstrip('0').rstrip('.')
    return f"{res}i" if is_imaginary else ("-" + res if value < 0 else res)

def format_coeff(val: float) -> str:
    """Removes trailing .0 for whole number coefficients."""
    return str(int(val)) if val.is_integer() else str(val)

def get_reduced_form_string(coefficients: dict[int, float], poly_degree: int) -> str:
    """Constructs the reduced form string exactly as shown in the PDF examples."""
    terms = []
    max_display_degree = max(0, poly_degree)
    
    for exp in sorted(coefficients.keys()):
        coeff = coefficients[exp]
        if coeff == 0.0 and exp > max_display_degree:
            continue
            
        if not terms:
            terms.append(f"{format_coeff(coeff)} * X^{exp}")
        else:
            sign = "+" if coeff >= 0 else "-"
            terms.append(f"{sign} {format_coeff(absolute_value(coeff))} * X^{exp}")
                
    return " ".join(terms) + " = 0" if terms else "0 * X^0 = 0"

def print_real_root(val: float) -> None:
    """Helper to format and print a single real root with its fraction representation."""
    if val == -0.0:
        val = 0.0
        
    f_val = f"{val:.6f}".rstrip('0').rstrip('.')
    print(f"{f_val}{format_fraction_bonus(val)}")

def solve_polynomial(coefficients: dict[int, float], verbose: bool = False) -> None:
    if verbose:
        print("[Verbose] Step 1: Moving all terms to the left side...")
        print("[Verbose] Step 2: Simplifying the coefficients...")

    polynomial_degree = 0
    for exp, coeff in sorted(coefficients.items(), reverse=True):
        if coeff != 0.0:
            polynomial_degree = exp
            break

    print(f"Reduced form: {get_reduced_form_string(coefficients, polynomial_degree)}")
    print(f"Polynomial degree: {polynomial_degree}")
    
    if polynomial_degree == 0:
        c = coefficients.get(0, 0.0)
        if verbose:
            print(f"[Verbose] Constant equation check: {c} = 0")
        print("Any real number is a solution." if c == 0.0 else "No solution.")
            
    elif polynomial_degree == 1:
        b, c = coefficients.get(1, 0.0), coefficients.get(0, 0.0)
        if verbose:
            print(f"[Verbose] Solving linear equation: {b} * X + {c} = 0")
        print("The solution is:")
        print_real_root(-c / b)
        
    elif polynomial_degree == 2:
        a, b, c = coefficients.get(2, 0.0), coefficients.get(1, 0.0), coefficients.get(0, 0.0)
        if verbose:
            print(f"[Verbose] Calculating discriminant: Delta = b^2 - 4ac")
        delta = (b * b) - (4.0 * a * c)
        if verbose:
            print(f"[Verbose] Delta = {delta}")
        
        if delta > 0:
            print("Discriminant is strictly positive, the two solutions are:")
            print_real_root((-b + custom_sqrt(delta)) / (2.0 * a))
            print_real_root((-b - custom_sqrt(delta)) / (2.0 * a))
        elif delta == 0:
            print("Discriminant is zero, the solution is:")
            print_real_root(-b / (2.0 * a))
        else:
            print("Discriminant is strictly negative, the two complex solutions are:")
            real_part = -b / (2.0 * a)
            imaginary_part = custom_sqrt(-delta) / (2.0 * a)
            r_str = "0" if real_part == -0.0 or real_part == 0.0 else format_complex_part(real_part)
            i_str = format_complex_part(imaginary_part, is_imaginary=True)
            print(f"{r_str} + {i_str}")
            print(f"{r_str} - {i_str}")
    else:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
