# ==========================================
# LESSON 4: LOOPS (FOR & WHILE)
# ==========================================

print("=== PYTHON LOOPS ===")

# WHAT ARE LOOPS?
# ===============
# Loops allow you to repeat code multiple times
# Two main types in Python: for loops and while loops

# 1. FOR LOOPS
# ============
# Used when you know how many times to repeat
# Or when you want to iterate through a collection

print("\n=== FOR LOOPS ===")

# Basic for loop with range()
print("Counting from 1 to 5:")
for i in range(1, 6):  # range(1, 6) generates 1, 2, 3, 4, 5
    print(f"Count: {i}")

print("\nCounting from 0 to 4:")
for i in range(5):  # range(5) generates 0, 1, 2, 3, 4
    print(f"Number: {i}")

# For loop with step
print("\nCounting by 2s:")
for i in range(0, 10, 2):  # range(start, stop, step)
    print(f"Even number: {i}")

# Countdown with negative step
print("\nCountdown:")
for i in range(10, 0, -1):  # Count down from 10 to 1
    print(f"T-minus {i}")
print("Blast off! 🚀")

# 2. LOOPING THROUGH STRINGS
# ===========================
print("\n=== LOOPING THROUGH STRINGS ===")

name = "Python"
print(f"Letters in '{name}':")
for letter in name:  # Iterate through each character
    print(f"Letter: {letter}")

# With index and character
print(f"\nLetters with positions:")
for i, letter in enumerate(name):  # enumerate() gives index and value
    print(f"Position {i}: {letter}")

# 3. LOOPING THROUGH LISTS
# =========================
print("\n=== LOOPING THROUGH LISTS ===")

# List of fruits
fruits = ["apple", "banana", "orange", "grape"]
print("Fruits in the list:")
for fruit in fruits:
    print(f"- {fruit}")

# With index
print("\nFruits with numbers:")
for i, fruit in enumerate(fruits, 1):  # Start numbering from 1
    print(f"{i}. {fruit}")

# Numbers list
numbers = [10, 20, 30, 40, 50]
print(f"\nOriginal numbers: {numbers}")

# Process each number
print("Doubled numbers:")
for num in numbers:
    doubled = num * 2
    print(f"{num} * 2 = {doubled}")

# 4. WHILE LOOPS
# ==============
# Used when you don't know how many times to repeat
# Continues while a condition is True

print("\n=== WHILE LOOPS ===")

# Basic while loop
count = 1
print("While loop counting to 5:")
while count <= 5:
    print(f"Count: {count}")
    count += 1  # Very important! Increment to avoid infinite loop

# While loop with user input simulation
print("\nGuessing game simulation:")
secret_number = 7
guess = 0  # Starting guess

attempts = 0
while guess != secret_number:
    attempts += 1
    # Simulating user guesses
    if attempts == 1:
        guess = 5
    elif attempts == 2:
        guess = 8
    elif attempts == 3:
        guess = 7
    
    print(f"Attempt {attempts}: Guess = {guess}")
    
    if guess < secret_number:
        print("Too low!")
    elif guess > secret_number:
        print("Too high!")
    else:
        print(f"Correct! You got it in {attempts} attempts!")

# 5. LOOP CONTROL: BREAK AND CONTINUE
# ====================================
print("\n=== LOOP CONTROL ===")

# BREAK - exits the loop immediately
print("Using break to exit early:")
for i in range(10):
    if i == 5:
        print(f"Breaking at {i}")
        break  # Exit the loop when i equals 5
    print(f"i = {i}")

# CONTINUE - skip to next iteration
print("\nUsing continue to skip even numbers:")
for i in range(10):
    if i % 2 == 0:  # If i is even
        continue  # Skip the rest of this iteration
    print(f"Odd number: {i}")

# 6. NESTED LOOPS
# ===============
# Loops inside other loops
print("\n=== NESTED LOOPS ===")

# Multiplication table
print("Multiplication table (3x3):")
for i in range(1, 4):  # Outer loop: rows
    for j in range(1, 4):  # Inner loop: columns
        result = i * j
        print(f"{i} x {j} = {result:2d}", end="  ")  # :2d formats to 2 digits
    print()  # New line after each row

# Creating a pattern
print("\nStar pattern:")
for i in range(1, 6):  # 5 rows
    for j in range(i):  # i stars per row
        print("*", end="")
    print()  # New line after each row

# 7. PRACTICAL EXAMPLES
# ======================
print("\n=== PRACTICAL EXAMPLES ===")

# Example 1: Sum of numbers
numbers = [10, 25, 30, 15, 20]
total = 0
print(f"Numbers: {numbers}")

for num in numbers:
    total += num  # Add each number to total
print(f"Sum: {total}")

# Example 2: Find maximum number
numbers = [45, 12, 78, 23, 56, 89, 34]
max_num = numbers[0]  # Start with first number

print(f"\nNumbers: {numbers}")
for num in numbers:
    if num > max_num:
        max_num = num
print(f"Maximum number: {max_num}")

# Example 3: Count vowels
sentence = "Hello World Python"
vowels = "aeiouAEIOU"
vowel_count = 0

print(f"\nSentence: '{sentence}'")
for char in sentence:
    if char in vowels:
        vowel_count += 1
print(f"Number of vowels: {vowel_count}")

# Example 4: Password strength checker
password = "Python123"
print(f"\nChecking password: '{password}'")

has_upper = False
has_lower = False
has_digit = False
has_special = False

for char in password:
    if char.isupper():
        has_upper = True
    elif char.islower():
        has_lower = True
    elif char.isdigit():
        has_digit = True
    elif char in "!@#$%^&*()":
        has_special = True

print(f"Has uppercase: {has_upper}")
print(f"Has lowercase: {has_lower}")
print(f"Has digits: {has_digit}")
print(f"Has special chars: {has_special}")

# 8. LOOP WITH ELSE
# =================
# Python's unique feature: else clause with loops
print("\n=== LOOP WITH ELSE ===")

# The else clause runs if the loop completes normally (no break)
numbers = [2, 4, 6, 8, 10]
print(f"Looking for odd number in: {numbers}")

for num in numbers:
    if num % 2 == 1:  # If odd number found
        print(f"Found odd number: {num}")
        break
else:
    print("No odd numbers found")  # This runs because no break occurred

# 9. COMMON LOOP PATTERNS
# ========================
print("\n=== COMMON PATTERNS ===")

# Pattern 1: Accumulator pattern
numbers = [1, 2, 3, 4, 5]
sum_total = 0
for num in numbers:
    sum_total += num
print(f"Sum of {numbers} = {sum_total}")

# Pattern 2: Filter pattern
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = []
for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)
print(f"Even numbers: {even_numbers}")

# Pattern 3: Transform pattern
names = ["alice", "bob", "charlie"]
capitalized_names = []
for name in names:
    capitalized_names.append(name.capitalize())
print(f"Capitalized names: {capitalized_names}")

# 10. LOOP EFFICIENCY TIPS
# =========================
print("\n=== EFFICIENCY TIPS ===")

# Tip 1: Use enumerate() instead of range(len())
items = ["apple", "banana", "cherry"]

# Less efficient:
print("Less efficient way:")
for i in range(len(items)):
    print(f"{i}: {items[i]}")

# More efficient:
print("More efficient way:")
for i, item in enumerate(items):
    print(f"{i}: {item}")

# Tip 2: Use 'in' for membership testing
vowels = "aeiou"
letter = "a"

# Good:
if letter in vowels:
    print(f"'{letter}' is a vowel")

# 11. AVOIDING COMMON MISTAKES
# =============================
print("\n=== COMMON MISTAKES TO AVOID ===")

# Mistake 1: Infinite loop (commented out to prevent hanging)
# count = 1
# while count <= 5:
#     print(count)
#     # Forgot to increment count - this would run forever!

# Mistake 2: Modifying list while iterating
numbers = [1, 2, 3, 4, 5]
print(f"Original: {numbers}")

# Wrong way (can cause issues):
# for num in numbers:
#     if num % 2 == 0:
#         numbers.remove(num)  # Don't modify list while iterating

# Right way:
numbers_copy = numbers.copy()  # Make a copy
for num in numbers_copy:
    if num % 2 == 0:
        numbers.remove(num)
print(f"After removing evens: {numbers}")

print("\n=== LESSON 4 COMPLETE ===")
print("You now understand loops and can repeat code efficiently!")
print("Next: Functions and Code Organization!") 