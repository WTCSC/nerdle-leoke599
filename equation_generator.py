"""
equation_generator.py

This module generates random math equations for the Nerdle game.
It creates valid equations in the format: number operator number = result
For example: 12+34=46 or 8*7=56
"""

########################################
# TODO: Import the appropriate modules #
########################################

import random

###########################################
# TODO: Implement the following functions #
###########################################

def generate_numbers_for_addition():
    """
    Generate two numbers that when added create an 8-character equation.
    Returns a tuple of (num1, num2, result)
    
    For addition, we want numbers that create 8 total characters
    Format: NN+NN=NN (2+1+2+1+2 = 8 characters)

    Example: (12, 34, 46) creates "12+34=46"
    """

    # Loop to get valid numbers that fit the criteria
    while True:

        # Generate two random two-digit numbers and make sure their sum is also two-digit
        num1 = random.randint(10, 89) 
        num2 = random.randint(10, 89)
        result = num1 + num2
        if 10 <= result <= 99:
            return (num1, num2, result)
        else:
            continue

def generate_numbers_for_subtraction():
    """
    Generate two numbers that when subtracted create an 8-character equation.
    Returns a tuple of (num1, num2, result)
    
    For subtraction, we want positive results only
    Format: NN-NN=NN (2+1+2+1+2 = 8 characters)

    Example: (56, 23, 33) creates "56-23=33"
    """

    # Loop to get valid numbers that fit the criteria
    while True:

        # Generate two random two-digit numbers and ensure the result is positive and two-digit
        num1 = random.randint(20, 99)
        num2 = random.randint(10, num1 - 10)
        result = num1 - num2
        if 10 < result < 100:
            return (num1, num2, result)
        else:
            continue


def generate_numbers_for_multiplication():
    """
    Generate two numbers that when multiplied create an 8-character equation.
    Returns a tuple of (num1, num2, result)
    
    For multiplication, we need exactly 8 characters
    Format: N*NN=NNN (1+1+2+1+3 = 8 characters)
    Single digit * two digit = three digit result
    
    Example: (3, 34, 102) creates "3*34=102" (8 characters)
    """

    # Loop to get valid numbers that fit the criteria
    while True:

        # Generate a single-digit number and a two-digit number and ensure the result is three-digit
        num1 = random.randint(2, 9)
        num2 = random.randint(10, 99)
        result = num1 * num2
        if 100 < result < 1000:
            return (num1, num2, result)
        else:
            continue

def generate_numbers_for_division():
    """
    Generate two numbers that when divided create an 8-character equation.
    Returns a tuple of (num1, num2, result)
    
    For division, we want exact division (no remainders)
    Format: NNN/NN=N (3+1+2+1+1 = 8 characters)
    We need to work backwards: result * divisor = dividend

    Example: (252, 36, 7) creates "252/36=7"
    """

    # Loop to get valid numbers that fit the criteria
    while True:

        # Generate a three-digit number and a two-digit number and ensure exact division
        num1 = random.randint(100, 999)
        num2 = random.randint(10, 99)
        if num1 % num2 == 0:

            # Ensure the result is a single-digit number
            result = num1 // num2
            if 1 <= result <= 9:
                return (num1, num2, result)
            else:
                continue
        else:
            continue
    
################################################################################
#  DO NOT EDIT BELOW THIS LINE, THESE FUNCTIONS ARE ALREADY COMPLETED FOR YOU  #
################################################################################

def generate_equation():
    """
    Generate a random math equation for the Nerdle game.
    
    Returns:
        str: A string representing a math equation (exactly 8 characters)
        
    Example return values:
        "12+34=46"
        "56-23=33" 
        "9*12=108" (Wait, this is 8 chars! 9*12=108)
        "84/4=21 " (This is 7 chars, need to pad or adjust)
    
    The equation will always be exactly 8 characters long and mathematically correct.
    """
    # Choose a random operation
    operations = ['+', '-', '*', '/']
    operation = random.choice(operations)
    
    # Generate numbers based on the operation
    if operation == '+':
        num1, num2, result = generate_numbers_for_addition()
        equation = f"{num1}+{num2}={result}"
    elif operation == '-':
        num1, num2, result = generate_numbers_for_subtraction()
        equation = f"{num1}-{num2}={result}"
    elif operation == '*':
        num1, num2, result = generate_numbers_for_multiplication()
        equation = f"{num1}*{num2}={result}"
    else:  # operation == '/'
        num1, num2, result = generate_numbers_for_division()
        equation = f"{num1}/{num2}={result}"
    
    # Ensure the equation is exactly 8 characters
    # If it's 7 characters, we might need to try again or adjust
    if len(equation) != 8:
        # For now, let's try again with a different operation
        return generate_equation()
    
    return equation

def validate_equation(equation):
    """
    Check if a given equation string is mathematically correct.
    
    Args:
        equation (str): The equation to validate (e.g., "12+34=46")
        
    Returns:
        bool: True if the equation is mathematically correct, False otherwise
        
    Example:
        validate_equation("12+34=46") returns True
        validate_equation("12+34=50") returns False
    """
    # Check if input is a string
    if not isinstance(equation, str):
        return False
        
    # Check if equation has the right format and length
    if len(equation) != 8:
        return False
    
    # Check if equation contains an equals sign
    if '=' not in equation:
        return False
    
    try:
        # Split the equation at the equals sign
        left_side, right_side = equation.split('=')
        
        # The right side should be the result
        expected_result = int(right_side)
        
        # Evaluate the left side of the equation
        # We need to be careful about the operation
        if '+' in left_side:
            parts = left_side.split('+')
            if len(parts) == 2:
                actual_result = int(parts[0]) + int(parts[1])
            else:
                return False
        elif '-' in left_side:
            parts = left_side.split('-')
            if len(parts) == 2:
                actual_result = int(parts[0]) - int(parts[1])
            else:
                return False
        elif '*' in left_side:
            parts = left_side.split('*')
            if len(parts) == 2:
                actual_result = int(parts[0]) * int(parts[1])
            else:
                return False
        elif '/' in left_side:
            parts = left_side.split('/')
            if len(parts) == 2:
                # Check for division by zero
                if int(parts[1]) == 0:
                    return False
                # Check if division is exact (no remainder)
                if int(parts[0]) % int(parts[1]) != 0:
                    return False
                actual_result = int(parts[0]) // int(parts[1])
            else:
                return False
        else:
            return False
        
        # Check if the calculated result matches the given result
        return actual_result == expected_result
        
    except ValueError:
        # If we can't convert strings to integers, the equation is invalid
        return False
    except ZeroDivisionError:
        # Division by zero is invalid
        return False