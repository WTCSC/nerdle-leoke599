"""
test_equation_generator.py

Unit tests for the equation_generator module.
These tests verify that equations are generated correctly and validation works properly.

To run these tests:
    pytest test_equation_generator.py

or to run with verbose output:
    pytest -v test_equation_generator.py
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from equation_generator import (
    generate_equation, 
    validate_equation, 
    generate_numbers_for_addition,
    generate_numbers_for_subtraction,
    generate_numbers_for_multiplication,
    generate_numbers_for_division
)


class TestEquationGeneration:
    """Test equation generation functions."""
    
    def test_generate_numbers_for_addition(self):
        """Test addition number generation."""
        for _ in range(10):  # Test multiple times due to randomness
            num1, num2, result = generate_numbers_for_addition()
            
            # Check that numbers are in expected range
            assert 10 <= num1 <= 99, f"num1 {num1} should be 2 digits"
            assert 10 <= num2 <= 99, f"num2 {num2} should be 2 digits"
            assert 10 <= result <= 99, f"result {result} should be 2 digits"
            
            # Check that math is correct
            assert num1 + num2 == result, f"{num1} + {num2} should equal {result}"
    
    def test_generate_numbers_for_subtraction(self):
        """Test subtraction number generation."""
        for _ in range(10):  # Test multiple times due to randomness
            num1, num2, result = generate_numbers_for_subtraction()
            
            # Check that numbers are in expected range
            assert 10 <= num1 <= 99, f"num1 {num1} should be 2 digits"
            assert 10 <= num2 <= num1, f"num2 {num2} should be <= num1 {num1}"
            assert 10 <= result <= 99, f"result {result} should be 2 digits"
            
            # Check that math is correct
            assert num1 - num2 == result, f"{num1} - {num2} should equal {result}"
    
    def test_generate_numbers_for_multiplication(self):
        """Test multiplication number generation."""
        for _ in range(10):  # Test multiple times due to randomness
            num1, num2, result = generate_numbers_for_multiplication()
            
            # Check that numbers are in expected range
            assert 2 <= num1 <= 9, f"num1 {num1} should be single digit 2-9"
            assert 10 <= num2 <= 99, f"num2 {num2} should be 2 digits"
            assert 100 <= result <= 999, f"result {result} should be 3 digits"
            
            # Check that math is correct
            assert num1 * num2 == result, f"{num1} * {num2} should equal {result}"
    
    def test_generate_numbers_for_division(self):
        """Test division number generation."""
        for _ in range(10):  # Test multiple times due to randomness
            num1, num2, result = generate_numbers_for_division()
            
            # Check that numbers are in expected range
            assert 100 <= num1 <= 999, f"num1 {num1} should be 3 digits"
            assert 10 <= num2 <= 99, f"num2 {num2} should be 2 digits"
            assert 2 <= result <= 9, f"result {result} should be single digit 2-9"
            
            # Check that math is correct
            assert num1 // num2 == result, f"{num1} / {num2} should equal {result}"
            assert num1 % num2 == 0, f"{num1} should be evenly divisible by {num2}"
    
    def test_generate_equation_format(self):
        """Test that generated equations have the correct format."""
        for _ in range(20):  # Test multiple equations
            equation = generate_equation()
            
            # Check length
            assert len(equation) == 8, f"Equation '{equation}' should be 8 characters"
            
            # Check that it contains exactly one equals sign
            assert equation.count('=') == 1, f"Equation '{equation}' should have exactly one ="
            
            # Check that it contains at least one operator
            operators = ['+', '-', '*', '/']
            has_operator = any(op in equation for op in operators)
            assert has_operator, f"Equation '{equation}' should contain an operator"
    
    def test_generate_equation_validity(self):
        """Test that all generated equations are mathematically valid."""
        for _ in range(20):  # Test multiple equations
            equation = generate_equation()
            assert validate_equation(equation), f"Generated equation '{equation}' should be valid"


class TestEquationValidation:
    """Test equation validation functions."""
    
    def test_validate_equation_correct_equations(self):
        """Test validation of correct equations."""
        valid_equations = [
            "12+34=46",
            "56-23=33", 
            "18*4=72",  # 8 characters
            "84/4=21"   # 7 characters - this should actually fail
        ]
        
        for equation in valid_equations:
            if len(equation) == 8:
                assert validate_equation(equation), f"Equation '{equation}' should be valid"
            else:
                assert not validate_equation(equation), f"Equation '{equation}' should be invalid (wrong length)"
    
    def test_validate_equation_incorrect_equations(self):
        """Test validation of incorrect equations."""
        invalid_equations = [
            "12+34=47",  # Wrong result
            "56-23=32",  # Wrong result
            "8*12=95",   # Wrong result
            "84/4=20"    # Wrong result
        ]
        
        for equation in invalid_equations:
            assert not validate_equation(equation), f"Equation '{equation}' should be invalid"
    
    def test_validate_equation_wrong_length(self):
        """Test validation of equations with wrong length."""
        wrong_length_equations = [
            "1+2=3",      # Too short
            "12+34=456",  # Too long
            "",           # Empty
            "12+34=4"     # Too short by 1
        ]
        
        for equation in wrong_length_equations:
            assert not validate_equation(equation), f"Equation '{equation}' should be invalid (wrong length)"
    
    def test_validate_equation_no_equals(self):
        """Test validation of equations without equals sign."""
        no_equals_equations = [
            "12+34+46",   # No equals
            "12-34-46",   # No equals
            "abcdefgh"    # No equals, invalid chars
        ]
        
        for equation in no_equals_equations:
            assert not validate_equation(equation), f"Equation '{equation}' should be invalid (no equals)"
    
    def test_validate_equation_division_by_zero(self):
        """Test validation handles division by zero."""
        assert not validate_equation("12/0=12"), "Division by zero should be invalid"
    
    def test_validate_equation_non_integer_division(self):
        """Test validation of division that doesn't result in whole numbers."""
        # These should be invalid because they don't result in whole numbers
        non_integer_divisions = [
            "15/2=7.5",  # This would be invalid format anyway
            "10/3=3"     # 10/3 = 3.33..., not 3
        ]
        
        # Note: The second example should be invalid because 10/3 != 3
        assert not validate_equation("10/3=3"), "Non-exact division should be invalid"
    
    def test_validate_equation_invalid_characters(self):
        """Test validation of equations with invalid characters."""
        invalid_char_equations = [
            "12+34=4a",   # Contains 'a'
            "1b+34=46",   # Contains 'b'
            "12&34=46"    # Contains '&'
        ]
        
        for equation in invalid_char_equations:
            assert not validate_equation(equation), f"Equation '{equation}' should be invalid (bad chars)"
    
    def test_validate_equation_multiple_operators(self):
        """Test validation of equations with multiple operators."""
        # These are complex cases that our simple parser might not handle
        # For now, our validation should reject these
        complex_equations = [
            "1+2+3=6",    # Multiple additions
            "12+-3=9",    # Mixed operators
            "12-+3=15"    # Mixed operators
        ]
        
        for equation in complex_equations:
            # Our current implementation should reject these as invalid
            # because they don't match our expected format
            result = validate_equation(equation)
            # We expect these to fail with our current simple parser
            assert not result, f"Complex equation '{equation}' should be invalid with current parser"

class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_validate_equation_empty_string(self):
        """Test validation of empty string."""
        assert not validate_equation(""), "Empty string should be invalid"
    
    def test_validate_equation_none_input(self):
        """Test validation with None input."""
        # With our improved validation, None input returns False instead of raising error
        assert not validate_equation(None), "None input should be invalid"
    
    def test_validate_equation_non_string_input(self):
        """Test validation with non-string input."""
        # With our improved validation, non-string input returns False instead of raising error
        assert not validate_equation(12345678), "Non-string input should be invalid"
    
    def test_generate_equation_consistency(self):
        """Test that generate_equation consistently produces valid equations."""
        # Generate many equations and ensure they're all valid
        equations = []
        for _ in range(50):
            equation = generate_equation()
            equations.append(equation)
            assert validate_equation(equation), f"Generated equation '{equation}' should be valid"
        
        # Check that we get some variety (not all the same)
        unique_equations = set(equations)
        assert len(unique_equations) > 1, "Should generate variety of equations"


# Test data for parameterized tests
VALID_TEST_EQUATIONS = [
    ("12+34=46", True),
    ("99-50=49", True), 
    ("6*15=90", False),  # Only 7 characters, invalid
    ("15-03=12", True),  # 8 characters, subtraction
    ("10+10=20", True)
]

INVALID_TEST_EQUATIONS = [
    ("12+34=47", False),  # Wrong math
    ("1+2=3", False),     # Too short
    ("12+34=456", False), # Too long
    ("12+34=4a", False),  # Invalid character
    ("12+34+46", False),  # No equals
    ("", False),          # Empty
    ("12/0=12", False)    # Division by zero
]


class TestParameterizedValidation:
    """Parameterized tests for equation validation."""
    
    @pytest.mark.parametrize("equation,expected", VALID_TEST_EQUATIONS)
    def test_valid_equations(self, equation, expected):
        """Test validation of known valid equations."""
        assert validate_equation(equation) == expected
    
    @pytest.mark.parametrize("equation,expected", INVALID_TEST_EQUATIONS)
    def test_invalid_equations(self, equation, expected):
        """Test validation of known invalid equations."""
        assert validate_equation(equation) == expected


if __name__ == "__main__":
    # Run tests when file is executed directly
    pytest.main([__file__, "-v"])