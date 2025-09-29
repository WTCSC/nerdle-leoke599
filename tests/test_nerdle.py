"""
test_nerdle.py

Integration tests for the main Nerdle game.
These tests verify that all components work together correctly.

To run these tests:
    pytest test_nerdle.py

or to run with verbose output:
    pytest -v test_nerdle.py
"""

import pytest
from unittest.mock import patch, MagicMock
import io
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nerdle import (
    display_welcome_message,
    get_player_guess,
    play_game,
    run_quick_test
)
import equation_generator
import game_engine


class TestWelcomeMessage:
    """Test welcome message display."""
    
    def test_display_welcome_message(self):
        """Test that welcome message displays without errors."""
        # Capture output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        display_welcome_message()
        
        # Reset stdout
        output = captured_output.getvalue()
        sys.stdout = sys.__stdout__
        
        # Check that key elements are present
        assert "NERDLE" in output
        assert "GAME RULES" in output
        assert "6 attempts" in output
        assert "\033[42m" in output  # Green background color
        assert "\033[43m" in output  # Yellow background color
        assert "\033[47m" in output  # Gray background color
        assert "0123456789+-*/=" in output


class TestPlayerInput:
    """Test player input handling."""
    
    @patch('builtins.input')
    def test_get_player_guess_valid_input(self, mock_input):
        """Test getting valid player input."""
        mock_input.return_value = "12+34=46"
        
        guess = get_player_guess()
        assert guess == "12+34=46"
    
    @patch('builtins.input')  
    @patch('builtins.print')
    def test_get_player_guess_invalid_length(self, mock_print, mock_input):
        """Test handling input with wrong length."""
        # First input too short, second input correct
        mock_input.side_effect = ["1+2=3", "12+34=46"]
        
        guess = get_player_guess()
        assert guess == "12+34=46"
        
        # Check that error message was printed
        mock_print.assert_any_call("Error: Guess must be exactly 8 characters. You entered 5 characters.")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_player_guess_invalid_characters(self, mock_print, mock_input):
        """Test handling input with invalid characters."""
        # First input has invalid char, second input correct
        mock_input.side_effect = ["12+34=4a", "12+34=46"]
        
        guess = get_player_guess()
        assert guess == "12+34=46"
        
        # Check that error message was printed about invalid characters
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        error_printed = any("Invalid characters found" in call for call in print_calls)
        assert error_printed, "Should print error about invalid characters"
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_player_guess_no_equals(self, mock_print, mock_input):
        """Test handling input without equals sign."""
        # First input no equals, second input correct
        mock_input.side_effect = ["12+34+46", "12+34=46"]
        
        guess = get_player_guess()
        assert guess == "12+34=46"
        
        # Check that error message was printed
        mock_print.assert_any_call("Error: Equation must have exactly one equals sign (=)")
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_get_player_guess_wrong_math(self, mock_print, mock_input):
        """Test handling input with wrong math."""
        # First input wrong math, second input correct
        mock_input.side_effect = ["12+34=47", "12+34=46"]
        
        guess = get_player_guess()
        assert guess == "12+34=46"
        
        # Check that error message was printed
        print_calls = [call.args[0] for call in mock_print.call_args_list]
        error_printed = any("not mathematically correct" in call for call in print_calls)
        assert error_printed, "Should print error about incorrect math"





class TestGameIntegration:
    """Test integration between all game components."""
    
    def test_equation_generator_integration(self):
        """Test that equation generator works with game engine."""
        # Generate an equation
        equation = equation_generator.generate_equation()
        
        # Validate it
        assert equation_generator.validate_equation(equation), "Generated equation should be valid"
        
        # Use it in game engine
        game_state = game_engine.create_new_game(equation)
        assert game_state['target'] == equation
        
        # The target equation should be a valid guess
        assert game_engine.is_valid_guess(equation), "Target equation should be valid guess"
    
    def test_full_game_workflow(self):
        """Test a complete game workflow."""
        # Generate target equation
        target = equation_generator.generate_equation()
        
        # Create game
        game_state = game_engine.create_new_game(target)
        assert not game_engine.is_game_over(game_state)
        
        # Make some guesses
        test_guesses = []
        for _ in range(3):  # Generate 3 different equations as guesses
            guess = equation_generator.generate_equation()
            if game_engine.is_valid_guess(guess):
                test_guesses.append(guess)
        
        # Process guesses
        for guess in test_guesses:
            if not game_engine.is_game_over(game_state):
                game_state, message = game_engine.process_guess(game_state, guess)
                assert isinstance(message, str), "Should return message string"
                assert game_state['attempts'] <= game_state['max_attempts']
        
        # Make winning guess
        if not game_engine.is_game_over(game_state):
            game_state, message = game_engine.process_guess(game_state, target)
            assert game_state['won'], "Should win with correct guess"
            assert game_engine.is_game_over(game_state), "Game should be over after winning"
    
    def test_game_validation_consistency(self):
        """Test that game engine and equation generator validation are consistent."""
        # Generate several equations
        equations = [equation_generator.generate_equation() for _ in range(10)]
        
        for equation in equations:
            # Both validators should agree
            eq_gen_valid = equation_generator.validate_equation(equation)
            game_eng_valid = game_engine.is_valid_guess(equation)
            
            assert eq_gen_valid == game_eng_valid, f"Validators disagree on '{equation}'"
            assert eq_gen_valid, f"Generated equation '{equation}' should be valid"


class TestQuickTest:
    """Test the quick test functionality."""
    
    def test_run_quick_test(self):
        """Test that quick test runs without errors."""
        # Capture output
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        run_quick_test()
        
        # Reset stdout
        output = captured_output.getvalue()
        sys.stdout = sys.__stdout__
        
        # Check that test output includes expected elements
        assert "Testing equation generation" in output
        assert "Testing game engine" in output
        assert "Generated:" in output
        assert "All components working correctly" in output


class TestGamePlaySimulation:
    """Test simulated game play scenarios."""
    
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('equation_generator.generate_equation')
    def test_winning_game_simulation(self, mock_generate, mock_print, mock_input):
        """Simulate a winning game."""
        target = "12+34=46"
        mock_generate.return_value = target
        
        # Simulate player input: wrong guess, then correct guess, then "no" to play again
        mock_input.side_effect = ["15+35=50", target, "no"]
        
        # This should run without errors and return False (don't play again)
        result = play_game()
        assert result == False, "Should return False when player chooses not to play again"
    
    @patch('builtins.input')
    @patch('builtins.print') 
    @patch('equation_generator.generate_equation')
    def test_losing_game_simulation(self, mock_generate, mock_print, mock_input):
        """Simulate a losing game."""
        target = "12+34=46"
        mock_generate.return_value = target
        
        # Simulate 6 wrong guesses, then "no" to play again
        wrong_guesses = ["15+35=50", "20+25=45", "10+30=40", "11+33=44", "16+36=52", "17+37=54"]
        mock_input.side_effect = wrong_guesses + ["no"]
        
        # This should run without errors and return False
        result = play_game()
        assert result == False, "Should return False when player chooses not to play again"
    
    @patch('builtins.input')
    @patch('builtins.print')
    @patch('equation_generator.generate_equation')
    def test_invalid_input_handling(self, mock_generate, mock_print, mock_input):
        """Test handling of invalid input during game."""
        target = "12+34=46"
        mock_generate.return_value = target
        
        # Simulate invalid input, then valid input, then correct answer, then "no"
        mock_input.side_effect = [
            "invalid",      # Invalid guess (will retry)
            "15+35=50",     # Valid wrong guess
            target,         # Correct answer
            "no"            # Don't play again
        ]
        
        result = play_game()
        assert result == False


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_empty_equation_handling(self):
        """Test handling of empty equation."""
        # This tests robustness of the system
        with patch('equation_generator.generate_equation', return_value=""):
            # The game should handle this gracefully
            try:
                game_state = game_engine.create_new_game("")
                assert game_state['target'] == ""
            except Exception as e:
                pytest.fail(f"Should handle empty equation gracefully, got: {e}")
    
    def test_malformed_game_state(self):
        """Test handling of malformed game state."""
        # Test with missing keys
        malformed_state = {'target': '12+34=46'}  # Missing other required keys
        
        with pytest.raises(KeyError):
            # This should raise KeyError when trying to access missing keys
            game_engine.is_game_over(malformed_state)


class TestModuleImports:
    """Test that modules can be imported correctly."""
    
    def test_equation_generator_import(self):
        """Test that equation_generator module imports correctly."""
        assert hasattr(equation_generator, 'generate_equation')
        assert hasattr(equation_generator, 'validate_equation')
    
    def test_game_engine_import(self):
        """Test that game_engine module imports correctly."""
        assert hasattr(game_engine, 'create_new_game')
        assert hasattr(game_engine, 'process_guess')
        assert hasattr(game_engine, 'is_game_over')
        assert hasattr(game_engine, 'get_feedback')
        assert hasattr(game_engine, 'is_valid_guess')
        assert hasattr(game_engine, 'get_valid_characters')


if __name__ == "__main__":
    # Run tests when file is executed directly
    pytest.main([__file__, "-v"])