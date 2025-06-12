# ==========================================
# LESSON 2: DATA TYPES & OPERATORS
# ==========================================

# PYTHON DATA TYPES
# ==================
# Python has several built-in data types

print("=== PYTHON DATA TYPES ===")

# 1. STRINGS (str)
# ================
# Text data enclosed in quotes
first_name = "Hamza"
last_name = 'Khan'
full_quote = """This is a 
multi-line string"""

print("String examples:")
print(f"First name: {first_name}")
print(f"Last name: {last_name}")
print(f"Multi-line: {full_quote}")

# String operations
print("\n--- String Operations ---")
greeting = "Hello"
name = "Python"

# Concatenation (joining strings)
message = greeting + " " + name + "!"
print(f"Concatenated: {message}")

# String repetition
repeated = "Ha" * 3  # Repeats "Ha" 3 times
print(f"Repeated: {repeated}")

# String length
print(f"Length of '{message}': {len(message)} characters")

# String methods (functions that work on strings)
sample_text = "  Python Programming  "
print(f"Original: '{sample_text}'")
print(f"Uppercase: '{sample_text.upper()}'")
print(f"Lowercase: '{sample_text.lower()}'")
print(f"Stripped: '{sample_text.strip()}'")  # Removes spaces
print(f"Replaced: '{sample_text.replace('Python', 'Java')}'")

# 2. NUMBERS
# ==========
print("\n=== NUMBERS ===")

# Integers (whole numbers)
age = 25
negative_num = -42
big_number = 1000000

print(f"Integer examples: {age}, {negative_num}, {big_number}")

# Floats (decimal numbers)
price = 19.99
pi = 3.14159
scientific = 2.5e3  # 2.5 * 10^3 = 2500

print(f"Float examples: {price}, {pi}, {scientific}")

# Complex numbers (advanced)
complex_num = 3 + 4j
print(f"Complex number: {complex_num}")

# Number operations
print("\n--- Number Operations ---")
x = 15
y = 4

print(f"x = {x}, y = {y}")
print(f"Addition: {x + y}")
print(f"Subtraction: {x - y}")
print(f"Multiplication: {x * y}")
print(f"Division: {x / y}")           # Result is always float
print(f"Floor Division: {x // y}")    # Integer division
print(f"Modulus: {x % y}")           # Remainder
print(f"Exponentiation: {x ** y}")   # x to the power of y

# Built-in math functions
import math  # Import math module for advanced functions

print(f"Absolute value of -10: {abs(-10)}")
print(f"Round 3.7: {round(3.7)}")
print(f"Round 3.14159 to 2 decimal places: {round(3.14159, 2)}")
print(f"Maximum of 5, 10, 3: {max(5, 10, 3)}")
print(f"Minimum of 5, 10, 3: {min(5, 10, 3)}")
print(f"Square root of 16: {math.sqrt(16)}")

# 3. BOOLEANS
# ===========
print("\n=== BOOLEANS ===")

# Boolean values: True or False (note the capital letters)
is_python_fun = True
is_difficult = False

print(f"Is Python fun? {is_python_fun}")
print(f"Is Python difficult? {is_difficult}")

# Boolean operations
print("\n--- Boolean Operations ---")
a = True
b = False

print(f"a = {a}, b = {b}")
print(f"a AND b: {a and b}")    # Both must be True
print(f"a OR b: {a or b}")      # At least one must be True
print(f"NOT a: {not a}")        # Opposite of a
print(f"NOT b: {not b}")        # Opposite of b

# 4. COMPARISON OPERATORS
# =======================
print("\n=== COMPARISON OPERATORS ===")

num1 = 10
num2 = 5
num3 = 10

print(f"num1 = {num1}, num2 = {num2}, num3 = {num3}")

# Comparison operators return Boolean values
print(f"num1 == num3 (equal): {num1 == num3}")           # True
print(f"num1 != num2 (not equal): {num1 != num2}")       # True
print(f"num1 > num2 (greater than): {num1 > num2}")      # True
print(f"num1 < num2 (less than): {num1 < num2}")         # False
print(f"num1 >= num3 (greater or equal): {num1 >= num3}") # True
print(f"num1 <= num2 (less or equal): {num1 <= num2}")   # False

# String comparisons
str1 = "apple"
str2 = "banana"
str3 = "apple"

print(f"\nString comparisons:")
print(f"'{str1}' == '{str3}': {str1 == str3}")  # True
print(f"'{str1}' < '{str2}': {str1 < str2}")    # True (alphabetical order)

# 5. LOGICAL OPERATORS
# ====================
print("\n=== LOGICAL OPERATORS ===")

# Combining conditions
age = 20
has_license = True
has_car = False

print(f"Age: {age}, Has License: {has_license}, Has Car: {has_car}")

# AND operator - all conditions must be True
can_drive_alone = age >= 18 and has_license
print(f"Can drive alone: {can_drive_alone}")

# OR operator - at least one condition must be True
can_travel = has_license or has_car
print(f"Can travel: {can_travel}")

# NOT operator - reverses the boolean value
is_minor = not (age >= 18)
print(f"Is minor: {is_minor}")

# Complex logical expressions
is_adult_driver = (age >= 18) and has_license and (has_car or True)
print(f"Is adult driver: {is_adult_driver}")

# 6. TYPE CONVERSION
# ==================
print("\n=== TYPE CONVERSION ===")

# Converting between types
str_number = "123"
int_number = int(str_number)  # String to integer
float_number = float(str_number)  # String to float

print(f"String: '{str_number}' (type: {type(str_number)})")
print(f"Integer: {int_number} (type: {type(int_number)})")
print(f"Float: {float_number} (type: {type(float_number)})")

# Number to string
age = 25
age_str = str(age)
print(f"Age as string: '{age_str}' (type: {type(age_str)})")

# Boolean conversions
print(f"\nBoolean conversions:")
print(f"bool(1): {bool(1)}")        # True
print(f"bool(0): {bool(0)}")        # False
print(f"bool('hello'): {bool('hello')}")  # True (non-empty string)
print(f"bool(''): {bool('')}")      # False (empty string)

print("\n=== LESSON 2 COMPLETE ===")
print("You now understand Python's basic data types and operations!")
print("Next: User Input and Conditional Statements!") 