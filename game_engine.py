"""
game_engine.py

This module handles the core game logic for Nerdle.
It manages the game state, validates user input, and provides feedback.
"""

########################################
# TODO: Import the appropriate modules #
########################################

import equation_generator

###########################################
# TODO: Implement the following functions #
###########################################

def is_valid_guess(guess):
    """
    Check if a player's guess is valid for Nerdle.
    
    A valid guess must:
    - Be exactly 8 characters long
    - Only contain valid characters (digits, +, -, *, /, =)
      - Hint: Use the get_valid_characters() function
    - Be a mathematically correct equation
      - Hint: Use the validate_equation() function from the equation_generator module
    - Have exactly one equals sign

    Args:
        guess (str): The player's guess
        
    Returns:
        bool: True if the guess is valid, False otherwise
    """

################################################################################
#  DO NOT EDIT BELOW THIS LINE, THESE FUNCTIONS ARE ALREADY COMPLETED FOR YOU  #
################################################################################

# ANSI color codes for terminal background colors
COLOR_GREEN = '\033[42m\033[30m'    # Green background, black text
COLOR_YELLOW = '\033[43m\033[30m'   # Yellow background, black text  
COLOR_GRAY = '\033[47m\033[30m'     # Light gray background, black text
COLOR_RESET = '\033[0m'             # Reset to default colors

def create_new_game(target_equation):
    """
    Create a new Nerdle game with the given target equation.
    
    Args:
        target_equation (str): The equation players need to guess
        
    Returns:
        dict: A dictionary representing the game state with keys:
              - 'target': the target equation
              - 'guesses': list of previous guesses
              - 'feedback': list of feedback for each guess
              - 'attempts': number of attempts made
              - 'max_attempts': maximum attempts allowed
              - 'game_over': whether the game has ended
              - 'won': whether the player has won
    """
    game_state = {
        'target': target_equation,
        'guesses': [],
        'feedback': [],
        'attempts': 0,
        'max_attempts': 6,
        'game_over': False,
        'won': False
    }
    
    return game_state

def get_feedback(guess, target):
    """
    Compare a guess with the target equation and return color-coded feedback.
    
    Args:
        guess (str): The player's guess
        target (str): The target equation
        
    Returns:
        list: A list of feedback for each character position:
              - 'G' for Green (correct character in correct position)
              - 'Y' for Yellow (correct character in wrong position)  
              - 'B' for Black/Gray (character not in target equation)
              
    Example:
        guess = "12+34=46", target = "15+31=46"
        returns ['G', 'B', 'G', 'B', 'B', 'G', 'G', 'G']
        (1=correct, 2=wrong, +=correct, 3=wrong, 4=wrong, ==correct, 4=correct, 6=correct)
    """
    # Handle edge case of empty target or mismatched lengths
    if len(target) != len(guess):
        return ['B'] * len(guess)
    
    feedback = []
    target_chars = list(target)  # Convert to list so we can modify it
    guess_chars = list(guess)
    
    # First pass: mark all exact matches (Green)
    for i in range(len(guess_chars)):
        if i < len(target_chars) and guess_chars[i] == target_chars[i]:
            feedback.append('G')
            target_chars[i] = None  # Mark as used
            guess_chars[i] = None   # Mark as processed
        else:
            feedback.append(None)   # Placeholder for now
    
    # Second pass: mark characters in wrong positions (Yellow)
    for i in range(len(guess_chars)):
        if guess_chars[i] is not None:  # Not already processed as Green
            if guess_chars[i] in target_chars:
                feedback[i] = 'Y'
                # Remove the first occurrence from target_chars
                target_chars[target_chars.index(guess_chars[i])] = None
            else:
                feedback[i] = 'B'  # Black/Gray - not in target
    
    return feedback

def format_feedback_display(guess, feedback):
    """
    Format the guess and feedback for display to the player using terminal background colors.
    
    Args:
        guess (str): The player's guess
        feedback (list): List of feedback codes ('G', 'Y', 'B')
        
    Returns:
        str: Formatted string showing the guess with colored backgrounds
        
    Example:
        guess = "12+34=46", feedback = ['G', 'B', 'G', 'Y', 'B', 'G', 'G', 'G']
        returns colored blocks for each character
    """
    display_parts = []
    
    for i in range(len(guess)):
        char = guess[i] 
        color = feedback[i]
        
        if color == 'G':
            display_parts.append(f"{COLOR_GREEN} {char} {COLOR_RESET}")
        elif color == 'Y':
            display_parts.append(f"{COLOR_YELLOW} {char} {COLOR_RESET}")
        else:  # color == 'B'
            display_parts.append(f"{COLOR_GRAY} {char} {COLOR_RESET}")
    
    return "".join(display_parts)

def format_feedback_plain(guess, feedback):
    """
    Format the guess and feedback for display without colors (for testing).
    
    Args:
        guess (str): The player's guess
        feedback (list): List of feedback codes ('G', 'Y', 'B')
        
    Returns:
        str: Formatted string showing the guess with text indicators
        
    Example:
        guess = "12+34=46", feedback = ['G', 'B', 'G', 'Y', 'B', 'G', 'G', 'G']
        returns "[1G][2B][+G][3Y][4B][=G][4G][6G]"
    """
    display_parts = []
    
    for i in range(len(guess)):
        char = guess[i] 
        color = feedback[i]
        display_parts.append(f"[{char}{color}]")
    
    return "".join(display_parts)

def format_feedback_plain(guess, feedback):
    """
    Format the guess and feedback for display without colors (for testing).
    
    Args:
        guess (str): The player's guess
        feedback (list): List of feedback codes ('G', 'Y', 'B')
        
    Returns:
        str: Formatted string showing the guess with text indicators
        
    Example:
        guess = "12+34=46", feedback = ['G', 'B', 'G', 'Y', 'B', 'G', 'G', 'G']
        returns "[1G][2B][+G][3Y][4B][=G][4G][6G]"
    """
    display_parts = []
    
    for i in range(len(guess)):
        char = guess[i] 
        color = feedback[i]
        display_parts.append(f"[{char}{color}]")
    
    return "".join(display_parts)

def process_guess(game_state, guess):
    """
    Process a player's guess and update the game state.
    
    Args:
        game_state (dict): Current game state
        guess (str): The player's guess
        
    Returns:
        dict: Updated game state
        str: Message to display to the player
        
    This function:
    1. Validates the guess
    2. Compares it with the target
    3. Updates game state
    4. Checks for win/loss conditions
    """
    # Check if game is already over
    if game_state['game_over']:
        return game_state, "Game is already over!"
    
    # Validate the guess
    if not is_valid_guess(guess):
        return game_state, "Invalid guess! Must be exactly 8 characters, mathematically correct equation."
    
    # Get feedback for the guess
    feedback = get_feedback(guess, game_state['target'])
    
    # Update game state
    game_state['guesses'].append(guess)
    game_state['feedback'].append(feedback)
    game_state['attempts'] += 1
    
    # Check if player won (all feedback is Green)
    if all(color == 'G' for color in feedback):
        game_state['won'] = True
        game_state['game_over'] = True
        message = f"Congratulations! You guessed it in {game_state['attempts']} attempts!"
    # Check if player ran out of attempts
    elif game_state['attempts'] >= game_state['max_attempts']:
        game_state['game_over'] = True
        message = f"Game over! The equation was: {game_state['target']}"
    else:
        # Game continues
        remaining = game_state['max_attempts'] - game_state['attempts']
        message = f"Try again! {remaining} attempts remaining."
    
    return game_state, message

def is_game_over(game_state):
    """
    Check if the game has ended.
    
    Args:
        game_state (dict): Current game state
        
    Returns:
        bool: True if game is over, False otherwise
    """
    return game_state['game_over']

def display_game_state(game_state):
    """
    Create a formatted display of the current game state.
    
    Args:
        game_state (dict): Current game state
        
    Returns:
        str: Formatted string showing all guesses and feedback
    """
    if not game_state['guesses']:
        return "No guesses yet. Make your first guess!"
    
    display_lines = []
    display_lines.append("Your guesses so far:")
    display_lines.append("")
    
    for i in range(len(game_state['guesses'])):
        guess = game_state['guesses'][i]
        feedback = game_state['feedback'][i]
        formatted_feedback = format_feedback_display(guess, feedback)
        display_lines.append(f"  {formatted_feedback}")
    
    display_lines.append("")
    remaining = game_state['max_attempts'] - game_state['attempts']
    display_lines.append(f"Attempts remaining: {remaining}")
    
    return "\n".join(display_lines)

def get_valid_characters():
    """
    Return a string containing all valid characters for Nerdle equations.
    
    Returns:
        str: A string of valid characters: "0123456789+-*/="
    """
    return "0123456789+-*/="