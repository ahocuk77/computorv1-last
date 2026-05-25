import sys
from parser import parse_equation
from solver import solve_polynomial

def print_help() -> None:
    """Prints a simple help menu explaining how to run the program."""
    print("Computor v1")
    print("Usage:")
    print("  python3 computor.py \"[equation]\" [options]")
    print("  python3 computor.py -h | --help")
    print("\nOptions:")
    print("  -v, --verbose    Show intermediate calculation steps.")
    print("\nExamples:")
    print("  python3 computor.py \"5 * X^0 + 4 * X^1 = 4 * X^0\"")
    print("  python3 computor.py \"5 + 4X + X^2 = X^2\" --verbose")

def main() -> None:
    """Main orchestrator handling arguments, help flag, and verbose option."""
    args = sys.argv[1:]
    
    if not args:
        try:
            equation_str = input("Please enter your equation: ")
            verbose = False
        except (KeyboardInterrupt, EOFError):
            return
    else:
        if any(h in args for h in ["-h", "--help"]):
            print_help()
            return
            
        verbose = False
        if "-v" in args or "--verbose" in args:
            verbose = True
            args = [a for a in args if a not in ["-v", "--verbose"]]
            
        if not args:
            print("Error: Missing equation argument.")
            return
            
        equation_str = args[0]

    try:
        coefficients = parse_equation(equation_str)
        solve_polynomial(coefficients, verbose=verbose)
    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()



# import sys


# from parser_mandatory import parse_equation
# from solver_mandatory import solve_polynomial

# def main():
#     if len(sys.argv) != 2:
#         print("Usage: python3 computor_mandatory.py <equation>")
#         sys.exit(1)

#     equation_str = sys.argv[1]

#     try:

#         coefficients = parse_equation(equation_str)

#         solve_polynomial(coefficients)
        
#     except ValueError as e:
#         print(f"{e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")

# if __name__ == "__main__":
#     main()