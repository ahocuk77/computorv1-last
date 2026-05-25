from math_custom import custom_sqrt, absolute_value

def format_coeff(val: float) -> str:
    """Removes the trailing .0 from whole numbers (e.g., 4.0 -> 4)"""
    return str(int(val)) if val.is_integer() else str(val)

def get_reduced_form_string(coefficients: dict[int, float], poly_degree: int) -> str:
    """MANDATORY: Prints results strictly in 'a * X^p' format."""
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
    """MANDATORY: Prints a clean floating point value without fraction representation."""
    if val == -0.0:
        val = 0.0
    f_val = f"{val:.6f}".rstrip('0').rstrip('.')
    print(f_val)

def solve_polynomial(coefficients: dict[int, float]) -> None:
    """MANDATORY: Resolves equations and produces basic solutions without verbose logs."""
    polynomial_degree = 0
    for exp, coeff in sorted(coefficients.items(), reverse=True):
        if coeff != 0.0:
            polynomial_degree = exp
            break

    print(f"Reduced form: {get_reduced_form_string(coefficients, polynomial_degree)}")
    print(f"Polynomial degree: {polynomial_degree}")
    
    if polynomial_degree == 0:
        c = coefficients.get(0, 0.0)
        print("Any real number is a solution." if c == 0.0 else "No solution.")
            
    elif polynomial_degree == 1:
        b, c = coefficients.get(1, 0.0), coefficients.get(0, 0.0)
        print("The solution is:")
        print_real_root(-c / b)
        
    elif polynomial_degree == 2:
        a, b, c = coefficients.get(2, 0.0), coefficients.get(1, 0.0), coefficients.get(0, 0.0)
        delta = (b * b) - (4.0 * a * c)
        
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
            
            if real_part == -0.0:
                real_part = 0.0
                
            r_str = f"{real_part:.6f}".rstrip('0').rstrip('.')
            i_str = f"{imaginary_part:.6f}".rstrip('0').rstrip('.')
            
            print(f"{r_str} + {i_str}i")
            print(f"{r_str} - {i_str}i")
    else:
        print("The polynomial degree is strictly greater than 2, I can't solve.")