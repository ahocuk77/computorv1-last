def custom_sqrt(number: float, tolerance: float = 1e-10) -> float:
    if number < 0:
        raise ValueError("Cannot calculate the real square root of a negative number.")
    if number == 0:
        return 0.0
    
    guess = number
    
    while True:
        next_guess = 0.5 * (guess + (number / guess))
        
        diff = next_guess - guess
        if diff < 0:
            diff = -diff
            
        if diff < tolerance:
            return next_guess
            
        guess = next_guess

def absolute_value(number: float) -> float:
    """Returns the absolute value of a given number."""
    return -number if number < 0 else number