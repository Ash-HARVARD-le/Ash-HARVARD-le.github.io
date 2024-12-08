from flask import session
from . import db
from .models import GameStats
import random

# Validate credit card number
def validate_credit_card(card_number):
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n
    # Valid if the following:
    return total % 10 == 0 

# Function for blackjack 
def calculate_hand_value(cards):
    # Input is cards

    # Initialize helper variables
    value = 0
    ace_count = 0

    # For every card check...
    for card in cards:
        # Get the card value (thanks to the API)
        card_value = card['value']
        if card_value in ['KING', 'QUEEN', 'JACK']:
            # All these cards have a value of 10
            value += 10
        elif card_value == 'ACE':
            # Aces are a special case, where they can be both 11 or 1, so do the folowing
            ace_count += 1
            value += 11  # Start by counting Aces as 11
        else:
            # Numbered cards have their value the same
            value += int(card_value)

    # Adjust for Aces (if the value exceeds 21, count Aces as 1)
    while value > 21 and ace_count:
        value -= 10
        ace_count -= 1

    # Return the value of a given hand
    return value

# Function used to clear a single game of blackjack
def clear_blackjack_game():
    session.pop('player_cards', None)
    session.pop('dealer_cards', None)
    session.pop('bet', None)
    session.pop('deck_id', None)
    session.pop('dealer_first_card_face_down', None)

# Function to clear the entire session with the user (used for logout, since if they logout, another user can't register and join the same game)
def clear_blackjack_session():
    clear_blackjack_game()
    
    session.pop('result', None)
    session.pop('final_player_cards', None)
    session.pop('final_dealer_cards', None)

# Helper function to add a game in the database for later use
def add_game_stat(user, game_type, bet, result):
    """
    Adds a new game session to the GameStats table for a user.
    """
    game_stats = GameStats(
        user_id=user.id,
        game_type=game_type,
        bet=bet,
        result=result
    )

    # Add the game stats to the session and commit to the database
    db.session.add(game_stats)
    db.session.commit()