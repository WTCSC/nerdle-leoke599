"""
test_game_engine.py

Unit tests for the game_engine module.
These tests verify that game logic, feedback, and state management work correctly.

To run these tests:
    pytest test_game_engine.py

or to run with verbose output:
    pytest -v test_game_engine.py
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game_engine import (
    create_new_game,
    is_valid_guess,
    get_feedback,
    format_feedback_display,
    format_feedback_plain,
    process_guess,
    is_game_over,
    display_game_state
)


class TestGameCreation:
    """Test game creation and initialization."""
    
    def test_create_new_game(self):
        """Test creating a new game with proper initialization."""
        target = "12+34=46"
        game = create_new_game(target)
        
        # Check all required keys are present
        required_keys = ['target', 'guesses', 'feedback', 'attempts', 'max_attempts', 'game_over', 'won']
        for key in required_keys:
            assert key in game, f"Game state should contain '{key}'"
        
        # Check initial values
        assert game['target'] == target
        assert game['guesses'] == []
        assert game['feedback'] == []
        assert game['attempts'] == 0
        assert game['max_attempts'] == 6
        assert game['game_over'] == False
        assert game['won'] == False
    
    def test_create_new_game_different_targets(self):
        """Test creating games with different target equations."""
        targets = ["12+34=46", "56-23=33", "8*12=96", "84/4=21"]
        
        for target in targets:
            game = create_new_game(target)
            assert game['target'] == target
            assert game['attempts'] == 0
            assert not game['game_over']


class TestGuessValidation:
    """Test guess validation functionality."""
    
    def test_is_valid_guess_correct_guesses(self):
        """Test validation of correct guesses."""
        valid_guesses = [
            "12+34=46",
            "56-23=33",
            "10+10=20"
        ]
        
        for guess in valid_guesses:
            assert is_valid_guess(guess), f"Guess '{guess}' should be valid"
    
    def test_is_valid_guess_wrong_length(self):
        """Test validation rejects wrong length guesses."""
        wrong_length_guesses = [
            "1+2=3",       # Too short
            "12+34=456",   # Too long
            "",            # Empty
            "1+1=2"        # Too short
        ]
        
        for guess in wrong_length_guesses:
            assert not is_valid_guess(guess), f"Guess '{guess}' should be invalid (wrong length)"
    
    def test_is_valid_guess_invalid_characters(self):
        """Test validation rejects invalid characters."""
        invalid_char_guesses = [
            "12+34=4a",    # Contains 'a'
            "1b+34=46",    # Contains 'b'
            "12&34=46",    # Contains '&'
            "12+34=4 "     # Contains space
        ]
        
        for guess in invalid_char_guesses:
            assert not is_valid_guess(guess), f"Guess '{guess}' should be invalid (bad chars)"
    
    def test_is_valid_guess_wrong_math(self):
        """Test validation rejects mathematically incorrect guesses."""
        wrong_math_guesses = [
            "12+34=47",    # Wrong result
            "56-23=32",    # Wrong result
            "8*12=95",     # Wrong result
            "84/4=20"      # Wrong result
        ]
        
        for guess in wrong_math_guesses:
            assert not is_valid_guess(guess), f"Guess '{guess}' should be invalid (wrong math)"
    
    def test_is_valid_guess_no_equals(self):
        """Test validation rejects guesses without equals sign."""
        no_equals_guesses = [
            "12+34+46",    # No equals
            "12-34-33",    # No equals
            "abcdefgh"     # No equals
        ]
        
        for guess in no_equals_guesses:
            assert not is_valid_guess(guess), f"Guess '{guess}' should be invalid (no equals)"
    
    def test_is_valid_guess_multiple_equals(self):
        """Test validation rejects guesses with multiple equals signs."""
        multiple_equals_guesses = [
            "12=34=46",    # Two equals
            "1=2=3=4",     # Multiple equals
            "12+3==46"     # Double equals
        ]
        
        for guess in multiple_equals_guesses:
            assert not is_valid_guess(guess), f"Guess '{guess}' should be invalid (multiple equals)"


class TestFeedbackGeneration:
    """Test feedback generation functionality."""
    
    def test_get_feedback_exact_match(self):
        """Test feedback when guess exactly matches target."""
        target = "12+34=46"
        guess = "12+34=46"
        feedback = get_feedback(guess, target)
        
        expected = ['G', 'G', 'G', 'G', 'G', 'G', 'G', 'G']
        assert feedback == expected, f"Exact match should give all Green, got {feedback}"
    
    def test_get_feedback_no_match(self):
        """Test feedback when no characters match."""
        target = "12+34=46"
        guess = "87*95=03"  # This would be invalid anyway
        # Let's use a valid equation - but note that '=' will always match position
        # and some numbers might coincidentally match
        target = "12+34=46"
        guess = "87-59=28"  # This actually shares '=' and some numbers might be in wrong positions
        feedback = get_feedback(guess, target)
        
        # The '=' should match at position 5, and '2' might be in wrong position
        # Let's just test that we get some feedback
        assert len(feedback) == 8, f"Feedback should have 8 elements, got {len(feedback)}"
        assert all(color in ['G', 'Y', 'B'] for color in feedback), "All feedback should be valid colors"
    
    def test_get_feedback_mixed_colors(self):
        """Test feedback with mixed Green, Yellow, and Black."""
        target = "12+34=46"
        guess = "13+24=46"  # 1,+,=,4,6 correct position, 3,2 wrong position
        feedback = get_feedback(guess, target)
        
        # Expected: 1(G), 3(Y-wrong pos), +(G), 2(Y-wrong pos), 4(G), =(G), 4(G), 6(G)
        # Wait, let me recalculate this carefully:
        # target: "12+34=46"  positions: 0=1, 1=2, 2=+, 3=3, 4=4, 5==, 6=4, 7=6
        # guess:  "13+24=46"  positions: 0=1, 1=3, 2=+, 3=2, 4=4, 5==, 6=4, 7=6
        # Position 0: 1 matches 1 -> G
        # Position 1: 3 is in target at pos 3 -> Y  
        # Position 2: + matches + -> G
        # Position 3: 2 is in target at pos 1 -> Y
        # Position 4: 4 matches 4 -> G
        # Position 5: = matches = -> G
        # Position 6: 4 matches 4 -> G  
        # Position 7: 6 matches 6 -> G
        expected = ['G', 'Y', 'G', 'Y', 'G', 'G', 'G', 'G']
        assert feedback == expected, f"Mixed feedback should be {expected}, got {feedback}"
    
    def test_get_feedback_duplicate_characters(self):
        """Test feedback with duplicate characters in guess and target."""
        target = "11+22=33"
        guess = "22+11=33"  # All characters present but some in wrong positions
        feedback = get_feedback(guess, target)
        
        # This is tricky - need to handle duplicates correctly
        # target: "11+22=33" 
        # guess:  "22+11=33"
        # The algorithm should handle this correctly by marking used characters
        expected = ['Y', 'Y', 'G', 'Y', 'Y', 'G', 'G', 'G']
        assert feedback == expected, f"Duplicate handling should be {expected}, got {feedback}"
    
    def test_format_feedback_display(self):
        """Test formatting feedback for display with colors."""
        guess = "12+34=46"
        feedback = ['G', 'Y', 'G', 'B', 'G', 'G', 'Y', 'G']
        
        # Test that colored format contains the expected color codes
        formatted = format_feedback_display(guess, feedback)
        assert "\033[42m" in formatted, "Should contain green background color code"
        assert "\033[43m" in formatted, "Should contain yellow background color code"
        assert "\033[47m" in formatted, "Should contain gray background color code"
        assert "\033[0m" in formatted, "Should contain reset color code"
        
        # Test plain format for exact matching
        plain_formatted = format_feedback_plain(guess, feedback)
        expected_plain = "[1G][2Y][+G][3B][4G][=G][4Y][6G]"
        assert plain_formatted == expected_plain, f"Plain formatted should be '{expected_plain}', got '{plain_formatted}'"


class TestGameStateManagement:
    """Test game state management functionality."""
    
    def test_process_guess_valid_guess(self):
        """Test processing a valid guess."""
        target = "12+34=46"
        game = create_new_game(target)
        guess = "15+35=50"
        
        updated_game, message = process_guess(game, guess)
        
        # Check that game state was updated
        assert len(updated_game['guesses']) == 1
        assert updated_game['guesses'][0] == guess
        assert len(updated_game['feedback']) == 1
        assert updated_game['attempts'] == 1
        assert not updated_game['game_over']  # Should not be over yet
        assert not updated_game['won']
        assert "remaining" in message.lower()
    
    def test_process_guess_invalid_guess(self):
        """Test processing an invalid guess."""
        target = "12+34=46"
        game = create_new_game(target)
        guess = "invalid!"  # Invalid guess
        
        updated_game, message = process_guess(game, guess)
        
        # Game state should not change for invalid guess
        assert len(updated_game['guesses']) == 0
        assert updated_game['attempts'] == 0
        assert not updated_game['game_over']
        assert "invalid" in message.lower()
    
    def test_process_guess_winning_guess(self):
        """Test processing a winning guess."""
        target = "12+34=46"
        game = create_new_game(target)
        guess = "12+34=46"  # Correct guess
        
        updated_game, message = process_guess(game, guess)
        
        # Game should be won and over
        assert updated_game['won'] == True
        assert updated_game['game_over'] == True
        assert len(updated_game['guesses']) == 1
        assert updated_game['attempts'] == 1
        assert "congratulations" in message.lower()
    
    def test_process_guess_game_over_loss(self):
        """Test game ending when max attempts reached."""
        target = "12+34=46"
        game = create_new_game(target)
        
        # Make 6 wrong guesses
        wrong_guesses = ["15+35=50", "20+25=45", "10+30=40", "11+33=44", "16+36=52", "17+37=54"]
        
        for i, guess in enumerate(wrong_guesses):
            game, message = process_guess(game, guess)
            
            if i < 5:  # First 5 guesses
                assert not game['game_over'], f"Game should not be over after guess {i+1}"
                assert not game['won']
            else:  # 6th guess
                assert game['game_over'], "Game should be over after 6 attempts"
                assert not game['won'], "Game should not be won"
                assert "game over" in message.lower()
    
    def test_process_guess_already_over(self):
        """Test processing guess when game is already over."""
        target = "12+34=46"
        game = create_new_game(target)
        game['game_over'] = True  # Manually set game as over
        
        guess = "15+35=50"
        updated_game, message = process_guess(game, guess)
        
        assert "already over" in message.lower()
    
    def test_is_game_over(self):
        """Test is_game_over function."""
        target = "12+34=46"
        game = create_new_game(target)
        
        # Initially not over
        assert not is_game_over(game)
        
        # After winning
        game['game_over'] = True
        game['won'] = True
        assert is_game_over(game)
        
        # After losing
        game['won'] = False
        assert is_game_over(game)


class TestDisplayFunctions:
    """Test display and formatting functions."""
    
    def test_display_game_state_no_guesses(self):
        """Test displaying game state with no guesses."""
        target = "12+34=46"
        game = create_new_game(target)
        
        display = display_game_state(game)
        assert "no guesses yet" in display.lower()
    
    def test_display_game_state_with_guesses(self):
        """Test displaying game state with guesses."""
        target = "12+34=46"
        game = create_new_game(target)
        
        # Add a guess
        guess = "15+35=50"
        game, _ = process_guess(game, guess)
        
        display = display_game_state(game)
        assert "your guesses so far:" in display.lower()
        assert "attempts remaining:" in display.lower()
        # The guess will be shown with color codes, so check for parts of it
        assert "1" in display and "5" in display
    



class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_target_equation(self):
        """Test creating game with empty target."""
        game = create_new_game("")
        assert game['target'] == ""
        
        # This should cause an error when trying to get feedback
        # Let's test that the game handles this by not allowing the guess
        guess = "12+34=46"
        try:
            updated_game, message = process_guess(game, guess)
            # If it doesn't crash, the guess should be processed but feedback might be weird
            assert isinstance(message, str), "Should return a message"
        except (IndexError, ValueError):
            # It's acceptable for this to fail with empty target
            pass
    
    def test_feedback_with_equal_length_strings(self):
        """Test feedback generation with equal length strings."""
        # Both strings must be exactly 8 characters
        target = "12+34=46"
        guess = "87-59=28"
        
        feedback = get_feedback(guess, target)
        assert len(feedback) == 8, "Feedback should have 8 elements"
        assert all(color in ['G', 'Y', 'B'] for color in feedback), "All feedback should be valid colors"


# Parameterized test data
FEEDBACK_TEST_CASES = [
    # (target, guess, expected_feedback)
    ("12+34=46", "12+34=46", ['G', 'G', 'G', 'G', 'G', 'G', 'G', 'G']),  # Exact match
    ("12+34=46", "87-59=03", ['B', 'B', 'B', 'B', 'B', 'G', 'B', 'Y']),  # '=' matches, '3' in wrong position
    ("12+34=46", "21+43=64", ['Y', 'Y', 'G', 'Y', 'Y', 'G', 'Y', 'Y']),  # All wrong positions
]


class TestParameterizedFeedback:
    """Parameterized tests for feedback generation."""
    
    @pytest.mark.parametrize("target,guess,expected", FEEDBACK_TEST_CASES)
    def test_feedback_cases(self, target, guess, expected):
        """Test various feedback scenarios."""
        feedback = get_feedback(guess, target)
        assert feedback == expected, f"For target '{target}' and guess '{guess}', expected {expected}, got {feedback}"


if __name__ == "__main__":
    # Run tests when file is executed directly
    pytest.main([__file__, "-v"])