"""
nerdle.py

Main game file for Nerdle - a Wordle clone with math equations.
This file handles the user interface and game loop.
"""

import equation_generator
import game_engine

def display_welcome_message():
    """Display the welcome message and game rules to the player."""
    print("=" * 60)
    print("             WELCOME TO NERDLE!")
    print("         A Math Equation Guessing Game")
    print("=" * 60)
    print()
    print("GAME RULES:")
    print("- Guess the 8-character math equation")
    print("- You have 6 attempts to get it right")
    print("- Each equation has the format: NN+NN=NN (or -, *, /)")
    print("- After each guess, you'll get color-coded feedback:")
    print("  * \033[42m\033[30m Green \033[0m: Correct character in correct position")
    print("  * \033[43m\033[30m Yellow \033[0m: Correct character but wrong position")
    print("  * \033[47m\033[30m Gray \033[0m: Character not in the target equation")
    print()
    print("EXAMPLE:")
    print("Target:   12+34=46")
    print("Guess:    15+35=50") 
    print("Feedback: \033[42m\033[30m 1 \033[0m\033[47m\033[30m 5 \033[0m\033[42m\033[30m + \033[0m\033[43m\033[30m 3 \033[0m\033[47m\033[30m 5 \033[0m\033[42m\033[30m = \033[0m\033[47m\033[30m 5 \033[0m\033[47m\033[30m 0 \033[0m")
    print()
    print("Valid characters: 0123456789+-*/=")
    print("=" * 60)
    print()


def get_player_guess():
    """
    Get a guess from the player with input validation.
    
    Returns:
        str: The player's guess (exactly 8 characters)
    """
    while True:
        print("Enter your guess (8 characters, e.g., 12+34=46):")
        guess = input("> ").strip()
        
        # Basic length check
        if len(guess) != 8:
            print(f"Error: Guess must be exactly 8 characters. You entered {len(guess)} characters.")
            continue
        
        # Check for valid characters
        valid_chars = game_engine.get_valid_characters()
        invalid_chars = []
        for char in guess:
            if char not in valid_chars:
                invalid_chars.append(char)
        
        if invalid_chars:
            print(f"Error: Invalid characters found: {invalid_chars}")
            print(f"Valid characters are: {valid_chars}")
            continue
        
        # Check for exactly one equals sign
        if guess.count('=') != 1:
            print("Error: Equation must have exactly one equals sign (=)")
            continue
        
        # Check if equation is mathematically correct
        if not equation_generator.validate_equation(guess):
            print("Error: Equation is not mathematically correct.")
            print("Make sure the math adds up! For example: 12+34=46")
            continue
        
        return guess





def play_game():
    """
    Main game loop for a single game of Nerdle.
    
    Returns:
        bool: True if player wants to play again, False otherwise
    """
    print("Generating your equation...")
    
    # Generate a random equation for the player to guess
    target_equation = equation_generator.generate_equation()
    
    # Create a new game
    game_state = game_engine.create_new_game(target_equation)
    
    print("Equation generated! Start guessing...")
    print()
    
    # Main game loop
    while not game_engine.is_game_over(game_state):
        # Display current game state
        print(game_engine.display_game_state(game_state))
        print()
        
        # Get player's guess
        guess = get_player_guess()
        
        # Process the guess
        game_state, message = game_engine.process_guess(game_state, guess)
        
        print()
        print("RESULT:", message)
        print()
        
        # If game is over, show final state
        if game_engine.is_game_over(game_state):
            print(game_engine.display_game_state(game_state))
            print()
            
            if game_state['won']:
                print("🎉 CONGRATULATIONS! You solved the equation! 🎉")
            else:
                print("😞 Better luck next time!")
                print(f"The correct equation was: {target_equation}")
    
    # Ask if player wants to play again
    print()
    while True:
        play_again = input("Would you like to play again? (y/n): ").strip().lower()
        if play_again in ['y', 'yes']:
            return True
        elif play_again in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' for yes or 'n' for no.")


def main():
    """
    Main function that runs the Nerdle game.
    Handles multiple games and the overall game experience.
    """
    display_welcome_message()
    
    games_played = 0
    games_won = 0
    
    # Keep playing until user wants to quit
    while True:
        games_played += 1
        print(f"\nGAME {games_played}")
        print("-" * 20)
        
        # Play one game
        play_again = play_game()
        
        # Update statistics (this is basic - could be expanded)
        # Note: We'd need to modify play_game() to return win/loss info
        # For now, let's keep it simple
        
        if not play_again:
            break
    
    # Display final statistics
    print("\n" + "=" * 40)
    print("           THANKS FOR PLAYING!")
    print("=" * 40)
    print(f"Games played: {games_played}")
    print("Come back anytime to exercise your math skills!")
    print("=" * 40)


def run_quick_test():
    """
    Quick test function to verify all modules work together.
    This function can be used for debugging and testing.
    """
    print("Running quick test of Nerdle components...")
    
    # Test equation generation
    print("\n1. Testing equation generation:")
    for i in range(3):
        equation = equation_generator.generate_equation()
        is_valid = equation_generator.validate_equation(equation)
        print(f"   Generated: {equation} (Valid: {is_valid})")
    
    # Test game engine
    print("\n2. Testing game engine:")
    target = "12+34=46"
    game = game_engine.create_new_game(target)
    print(f"   Created game with target: {target}")
    
    # Test a guess
    guess = "15+35=50"
    game, message = game_engine.process_guess(game, guess)
    print(f"   Processed guess '{guess}': {message}")
    
    print("\n✅ All components working correctly!")


# Run the game when this file is executed directly
if __name__ == "__main__":
    # Uncomment the next line if you want to run a quick test first
    # run_quick_test()
    
    # Run the main game
    main()