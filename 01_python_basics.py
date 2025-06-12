# ========================================
# LESSON 1: PYTHON BASICS & INTRODUCTION
# ========================================

# What is Python?
# Python is a high-level, interpreted programming language
# Known for its simplicity and readability

# 1. COMMENTS
# ============
# Single line comments start with #
# They help explain your code

"""
Multi-line comments (docstrings)
Can span multiple lines
Used for documentation
"""

# 2. PRINT FUNCTION
# =================
# The print() function displays output to the console
print("Hello, World!")  # This prints text to screen
print("Welcome to Python!")
print()  # This prints an empty line

# 3. VARIABLES
# ============
# Variables store data values
# No need to declare variable type in Python

# String variables (text)
name = "Hamza"  # String enclosed in quotes
message = 'Python is awesome!'  # Single or double quotes work

# Numeric variables
age = 25  # Integer (whole number)
height = 5.8  # Float (decimal number)
temperature = -10  # Negative numbers

# Boolean variables (True/False)
is_student = True
is_graduated = False

# 4. DISPLAYING VARIABLES
# =======================
print("Name:", name)
print("Age:", age)
print("Height:", height)
print("Is student?", is_student)

# 5. STRING FORMATTING
# ====================
# f-strings (formatted string literals) - Modern way
print(f"Hello, my name is {name} and I am {age} years old")

# .format() method - Alternative way
print("My height is {} feet".format(height))

# % formatting - Old way (still used)
print("Temperature is %d degrees" % temperature)

# 6. VARIABLE TYPES
# =================
# Python determines type automatically
print("\n=== VARIABLE TYPES ===")
print("Type of name:", type(name))      # <class 'str'>
print("Type of age:", type(age))        # <class 'int'>
print("Type of height:", type(height))  # <class 'float'>
print("Type of is_student:", type(is_student))  # <class 'bool'>

# 7. BASIC ARITHMETIC OPERATIONS
# ===============================
print("\n=== BASIC MATH ===")
a = 10
b = 3

print(f"Addition: {a} + {b} = {a + b}")        # 13
print(f"Subtraction: {a} - {b} = {a - b}")     # 7
print(f"Multiplication: {a} * {b} = {a * b}")  # 30
print(f"Division: {a} / {b} = {a / b}")        # 3.333...
print(f"Floor Division: {a} // {b} = {a // b}") # 3 (rounded down)
print(f"Modulus (remainder): {a} % {b} = {a % b}") # 1
print(f"Exponentiation: {a} ** {b} = {a ** b}") # 1000

# 8. VARIABLE REASSIGNMENT
# ========================
# Variables can be changed
score = 100
print(f"Initial score: {score}")

score = score + 50  # Add 50 to current score
print(f"After bonus: {score}")

score += 25  # Shorthand for score = score + 25
print(f"After another bonus: {score}")

# 9. MULTIPLE VARIABLE ASSIGNMENT
# ===============================
# Assign multiple variables at once
x, y, z = 10, 20, 30
print(f"x={x}, y={y}, z={z}")

# Assign same value to multiple variables
a = b = c = 100
print(f"a={a}, b={b}, c={c}")

print("\n=== LESSON 1 COMPLETE ===")
print("Next: Data Types and Operators!") 