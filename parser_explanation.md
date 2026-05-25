# Parser Module Explanation

This document explains the working logic of the `parser.py` module in the **Computor V1** project.

---

## Overview
The `parser.py` file is responsible for taking a raw string representing a polynomial equation (e.g., `"5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0"`) and converting it into a dictionary of coefficients mapped to their respective exponents (e.g., `{0: 4.0, 1: 4.0, 2: -9.3}`).

---

## 1. `clean_and_tokenize(equation_str)`
This function cleans up the input equation and performs initial safety/syntax validation.

* **Whitespace Removal:** Removes all whitespaces (`\s+`) from the input.
* **Lexical Validation:** Ensures only valid polynomial characters (`0-9`, `x`, `X`, `.`, `+`, `-`, `*`, `^`, `=`) are used.
* **Equality Sign check:** Validates that there is exactly one `=` sign and that neither the left nor right side is empty.
* **Consecutive Operator Validation:** Prevents syntax errors like `++`, `+-`, `*+`, `==`, `--` or duplicate operators (`**`, `^^`).
* **Mathematical Limits:** Restricts polynomial exponents to be non-negative whole numbers (blocks float exponents like `X^1.5` and negative exponents like `X^-1`).

---

## 2. `parse_term(term_str)`
This function takes a single term (e.g., `"-9.3*X^2"`, `"+5"`, `"-X"`, or `"X"`) and extracts its numerical coefficient and integer exponent.

* **Variable Standardization:** Replaces lowercase `x` with uppercase `X`.
* **Single variable rule:** Ensures there is at most one `X` in a single term (rejects inputs like `5XX`).
* **Constants Handling:** If there is no `X` in the term, it treats it as a constant number (coefficient `float(term_str)`, exponent `0`).
* **Coefficient Parsing:** Splits the term by `X`. If the left side (coefficient) is empty or `+`, it is treated as `1.0`. If it is `-`, it is treated as `-1.0`. Otherwise, it removes any trailing `*` and parses it as a float.
* **Exponent Parsing:** On the right side of `X` (exponent), if empty, it defaults to `1` (implied power of 1). Otherwise, it removes the leading `^` and parses it as an integer.

---

## 3. `parse_equation(equation_str)`
This function is the main entry point for the parser, orchestrating the whole tokenization and splitting workflow.

* **LHS and RHS Split:** Splitting the validated, cleaned equation string into Left-Hand Side (LHS) and Right-Hand Side (RHS).
* **Sign-Preserving Splitting:** Splitting each side into individual terms by detecting sign boundary positions (`+` or `-`) without losing the operator sign.
* **Aggregating Coefficients:**
  * Iterates through the LHS terms and **adds** their parsed coefficients to the degree-mapping dictionary.
  * Iterates through the RHS terms and **subtracts** their parsed coefficients from the degree-mapping dictionary (mathematically moving all RHS terms to the LHS to align the equation as `= 0`).
