# ==========================================
# LESSON 3: USER INPUT & CONDITIONAL STATEMENTS
# ==========================================

print("=== USER INPUT & CONDITIONALS ===")

# 1. GETTING USER INPUT
# ======================
# The input() function gets text from the user
# It always returns a string, even if user types numbers

print("Let's learn about user input!")

# Basic input
# name = input("What's your name? ")
# print(f"Hello, {name}!")

# For this demo, we'll use predefined values
# But you can uncomment the lines above to test interactively
print("(Demo mode - using predefined values)")
name = "Hamza"  # Simulating user input
print(f"What's your name? {name}")
print(f"Hello, {name}!")

# 2. INPUT WITH TYPE CONVERSION
# =============================
# input() always returns string, so we need to convert for numbers

print("\n=== INPUT TYPE CONVERSION ===")

# Getting a number from user
# age_str = input("Enter your age: ")
age_str = "20"  # Simulating user input
print(f"Enter your age: {age_str}")

# Convert string to integer
age = int(age_str)
print(f"You are {age} years old")
print(f"Type of age: {type(age)}")

# Getting a decimal number
# height_str = input("Enter your height in feet: ")
height_str = "5.8"  # Simulating user input
print(f"Enter your height in feet: {height_str}")

height = float(height_str)
print(f"Your height is {height} feet")

# 3. CONDITIONAL STATEMENTS (if, elif, else)
# ===========================================
print("\n=== CONDITIONAL STATEMENTS ===")

# Simple if statement
age = 20
print(f"Age: {age}")

if age >= 18:
    print("You are an adult!")  # This runs if condition is True

# if-else statement
age = 15
print(f"\nAge: {age}")

if age >= 18:
    print("You are an adult!")
else:
    print("You are a minor!")  # This runs if condition is False

# if-elif-else statement (multiple conditions)
score = 85
print(f"\nTest Score: {score}")

if score >= 90:
    print("Grade: A (Excellent!)")
elif score >= 80:
    print("Grade: B (Good job!)")  # This will run
elif score >= 70:
    print("Grade: C (Not bad)")
elif score >= 60:
    print("Grade: D (Need improvement)")
else:
    print("Grade: F (Study harder)")

# 4. COMPLEX CONDITIONS
# =====================
print("\n=== COMPLEX CONDITIONS ===")

age = 22
has_license = True
has_car = True

print(f"Age: {age}, Has License: {has_license}, Has Car: {has_car}")

# Multiple conditions with AND
if age >= 18 and has_license:
    print("You can drive!")
    
    # Nested if statement
    if has_car:
        print("You can drive your own car!")
    else:
        print("You need to borrow or rent a car.")
else:
    print("You cannot drive yet.")

# Multiple conditions with OR
weather = "rainy"
has_umbrella = False

print(f"\nWeather: {weather}, Has Umbrella: {has_umbrella}")

if weather == "sunny" or has_umbrella:
    print("Good to go outside!")
else:
    print("Better stay inside or get an umbrella!")

# 5. COMPARISON OPERATORS IN CONDITIONS
# =====================================
print("\n=== COMPARISON EXAMPLES ===")

password = "python123"
user_input = "python123"  # Simulating user input

print(f"Checking password: '{user_input}'")

if user_input == password:
    print("✓ Password correct! Access granted.")
else:
    print("✗ Wrong password! Access denied.")

# Number comparisons
temperature = 25
print(f"\nTemperature: {temperature}°C")

if temperature > 30:
    print("It's hot! 🌡️")
elif temperature > 20:
    print("Nice weather! ☀️")  # This will run
elif temperature > 10:
    print("A bit cool 🌤️")
else:
    print("It's cold! ❄️")

# 6. STRING COMPARISONS
# =====================
print("\n=== STRING COMPARISONS ===")

day = "saturday"
print(f"Today is: {day}")

# String equality (case sensitive)
if day == "saturday":
    print("Weekend! Time to relax! 🎉")
elif day == "sunday":
    print("Sunday funday! 🏖️")
else:
    print("It's a weekday. Time to work! 💼")

# Case-insensitive comparison
user_response = "YES"
print(f"\nDo you want to continue? {user_response}")

if user_response.lower() == "yes":  # Convert to lowercase for comparison
    print("Great! Let's continue.")
elif user_response.lower() == "no":
    print("Okay, stopping here.")
else:
    print("Please answer yes or no.")

# 7. CHECKING MULTIPLE VALUES
# ===========================
print("\n=== CHECKING MULTIPLE VALUES ===")

favorite_color = "blue"
print(f"Your favorite color: {favorite_color}")

# Check if value is in a list of options
if favorite_color in ["red", "blue", "green"]:
    print("That's a primary color!")
else:
    print("That's not a primary color.")

# Check if NOT in a list
day_of_week = "saturday"
print(f"Day: {day_of_week}")

if day_of_week not in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
    print("It's the weekend! 🎊")
else:
    print("It's a weekday.")

# 8. BOOLEAN CONDITIONS
# =====================
print("\n=== BOOLEAN CONDITIONS ===")

is_logged_in = True
is_premium_user = False

print(f"Logged in: {is_logged_in}, Premium: {is_premium_user}")

# Direct boolean check
if is_logged_in:  # Same as: if is_logged_in == True:
    print("Welcome back!")
    
    if is_premium_user:
        print("Enjoy your premium features! ⭐")
    else:
        print("Consider upgrading to premium! 💎")
else:
    print("Please log in first.")

# Negation
if not is_premium_user:  # Same as: if is_premium_user == False:
    print("You are using the free version.")

# 9. PRACTICAL EXAMPLE: SIMPLE CALCULATOR
# ========================================
print("\n=== PRACTICAL EXAMPLE: CALCULATOR ===")

# Simulating user input for calculator
num1 = 10
num2 = 5
operation = "+"

print(f"Number 1: {num1}")
print(f"Number 2: {num2}")
print(f"Operation: {operation}")

if operation == "+":
    result = num1 + num2
    print(f"Result: {num1} + {num2} = {result}")
elif operation == "-":
    result = num1 - num2
    print(f"Result: {num1} - {num2} = {result}")
elif operation == "*":
    result = num1 * num2
    print(f"Result: {num1} * {num2} = {result}")
elif operation == "/":
    if num2 != 0:  # Check for division by zero
        result = num1 / num2
        print(f"Result: {num1} / {num2} = {result}")
    else:
        print("Error: Cannot divide by zero!")
else:
    print("Error: Unknown operation!")

# 10. COMMON MISTAKES TO AVOID
# =============================
print("\n=== COMMON MISTAKES ===")

# 1. Using = instead of == for comparison
x = 5
print(f"x = {x}")

# Wrong: if x = 5:  # This would cause an error
# Correct:
if x == 5:
    print("✓ Correct: x equals 5")

# 2. Forgetting indentation
if True:
    print("✓ This is properly indented")
    print("✓ This too")
# print("This would be outside the if block")

# 3. Comparing different types
age_str = "20"
age_num = 20

print(f"age_str = '{age_str}' (type: {type(age_str)})")
print(f"age_num = {age_num} (type: {type(age_num)})")

if age_str == str(age_num):  # Convert to same type
    print("✓ Ages are equal (after type conversion)")

print("\n=== LESSON 3 COMPLETE ===")
print("You now understand user input and conditional statements!")
print("Next: Loops and Repetition!") 