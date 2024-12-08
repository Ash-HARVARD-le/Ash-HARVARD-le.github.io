from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user
import requests
from . import db
from .models import User, GameStats
from .helpers import calculate_hand_value, clear_blackjack_session, clear_blackjack_game, add_game_stat

# This is for pages with less IMPORTANT personal information
views = Blueprint('views', __name__)

# Load the home aka index route
@views.route('/')
@login_required
def index():
    return render_template("index.html", user=current_user)

# Load the deposit page
@views.route('/deposit')
@login_required
def deposit_page():
    return render_template("deposit.html", user=current_user, huid_locked=current_user.huid_locked)

# RECORDS PAGE!!!
@views.route('/records')
@login_required
def records():
    # Helper variable
    all_game_types = ['Blackjack', 'Slots', 'Roulette']

    # TIME TO QUERY WOOOOOOOOOOOOO

    # Total games played (count of GameStats entries for the user)
    total_games_played = db.session.query(db.func.count(GameStats.id)).filter(GameStats.user_id == current_user.id).scalar()

    # Total earnings and total losses
    total_earnings = db.session.query(db.func.sum(db.case(
        (GameStats.result == 'Win', GameStats.bet),  # Earnings
        else_=0  # Default value: 0 if no result
    )).label('earnings')).filter(GameStats.user_id == current_user.id).scalar() or 0

    total_losses = db.session.query(db.func.sum(db.case(
        (GameStats.result == 'Lose', GameStats.bet),  # Losses
        else_=0  # Default value: 0 if no result
    )).label('losses')).filter(GameStats.user_id == current_user.id).scalar() or 0

    # Biggest bet placed and won
    biggest_win = db.session.query(db.func.max(GameStats.bet)).filter(
        GameStats.user_id == current_user.id, GameStats.result == 'Win').scalar() or 0
    
    # Biggest loss version
    biggest_loss = db.session.query(db.func.max(GameStats.bet)).filter(
        GameStats.user_id == current_user.id, GameStats.result == 'Lose').scalar() or 0

    # Favorite game (most played game)
    favorite_game = db.session.query(GameStats.game_type, db.func.count(GameStats.id).label('count')).filter(
        GameStats.user_id == current_user.id).group_by(GameStats.game_type).order_by(db.func.count(GameStats.id).desc()).first()

    # Least favorite game (least played game, excludes games not played)
    least_favorite_game = db.session.query(GameStats.game_type, db.func.count(GameStats.id).label('count')).filter(
        GameStats.user_id == current_user.id).group_by(GameStats.game_type).order_by(db.func.count(GameStats.id)).first()

    # Luckiest game (highest win percentage)
    luckiest_game = db.session.query(
        GameStats.game_type,
        (db.func.sum(db.case(
            (GameStats.result == 'Win', 1),  # Wins
            else_=0
        )) * 100 / db.func.nullif(db.func.count(GameStats.id), 0)).label('win_percentage')
    ).filter(GameStats.user_id == current_user.id).group_by(GameStats.game_type).order_by(
        (db.func.sum(db.case(
            (GameStats.result == 'Win', 1),  # Wins
            else_=0
        )) * 100 / db.func.nullif(db.func.count(GameStats.id), 0)).desc()).first()

    # Unluckiest game (highest loss percentage)
    unluckiest_game = db.session.query(
        GameStats.game_type,
        (db.func.sum(db.case(
            (GameStats.result == 'Lose', 1),  # Losses
            else_=0
        )) * 100 / db.func.nullif(db.func.count(GameStats.id), 0)).label('loss_percentage')
    ).filter(GameStats.user_id == current_user.id).group_by(GameStats.game_type).order_by(
        (db.func.sum(db.case(
            (GameStats.result == 'Lose', 1),  # Losses
            else_=0
        )) * 100 / db.func.nullif(db.func.count(GameStats.id), 0)).desc()).first()

    # Stats for each game type
    game_stats = db.session.query(
        GameStats.game_type,
        db.func.sum(db.case(
            (GameStats.result == 'Win', 1),  # Wins
            else_=0
        )).label('games_won'),
        db.func.sum(db.case(
            (GameStats.result == 'Lose', 1),  # Losses
            else_=0
        )).label('games_lost'),
        db.func.sum(db.case(
        (GameStats.result == 'Tie', 1),  # Ties
        else_=0
        )).label('games_tied')
    ).filter(GameStats.user_id == current_user.id).group_by(GameStats.game_type).all()

    # Store information and pass it over to the html and use
    game_stats_dict = {game.game_type: game for game in game_stats}
    for game_type in all_game_types:
        if game_type not in game_stats_dict:
            # Add a default entry with zero counts for missing game types
            game_stats_dict[game_type] = {
                'game_type': game_type,
                'games_won': 0,
                'games_lost': 0,
                'games_tied': 0
            }

    return render_template('records.html', user=current_user,
                           total_games_played=total_games_played,
                           total_earnings=total_earnings,
                           total_losses=total_losses,
                           biggest_win=biggest_win,
                           biggest_loss=biggest_loss,
                           favorite_game=favorite_game,
                           least_favorite_game=least_favorite_game,
                           luckiest_game=luckiest_game,
                           unluckiest_game=unluckiest_game,
                           game_stats=game_stats_dict)

# LEADERBOARD PAGE
@views.route('/leaderboard')
@login_required
def leaderboard():
    # QUERY USERS BASED ON THE MOST EARNED FROM GAMBLING (not just by how much cash they have)
    # Time to see who's really the best gambler
    users = db.session.query(
        User,  # Get the User object itself
        db.func.sum(db.case(
            (GameStats.result == 'Win', GameStats.bet),  # Win: add the bet value
            (GameStats.result == 'Lose', -GameStats.bet),  # Lose: subtract the bet value
            else_=0  # Default value: 0 if no result
        )).label('total_earnings')  # Calculate total earnings
    ).join(GameStats, GameStats.user_id == User.id, isouter=True) \
     .group_by(User.id) \
     .order_by(db.func.sum(db.case( 
         (GameStats.result == 'Win', GameStats.bet),
         (GameStats.result == 'Lose', -GameStats.bet),
         else_=0
     )).desc()).all() # Order them by most earned first

    # Pass the users and their total earnings to the template
    return render_template('leaderboard.html', users=users)

# Time for the actual games

# Blackjack game
@views.route('/blackjack', methods=['GET', 'POST'])
@login_required
def blackjack():
    # If just arriving on page, check if they're in the middle of a game, if not, clear the session (helpful for after finishing a game)
    if request.method == 'GET':
        if not session.get('player_cards'):
            clear_blackjack_session()

    # Handle post requests
    if request.method == 'POST':
        # Deck id is used for the API calls
        deck_id = session.get('deck_id', None)
        action = request.form.get('action')  # Action can be 'bet', 'hit', or 'stand' (nothing else...)

        # If no deck has been assigned it means a round has not started
        if not deck_id:
            # Therefore the only action here is bet
            if action == 'bet':
                # Get bet
                bet = request.form['bet']

                # Validate the bet
                try:
                    check_float = float(bet)
                    # Check if the bet is a positive number
                    if check_float <= 0:
                        return render_template("apology.html", user=current_user, message="Invalid Bet.")
                    # Check if the bet is greater than available cash
                    elif check_float > current_user.cash:
                        return render_template("apology.html", user=current_user, message="Can't Place Bet. You Are Too Poor.")
                    # Check if the bet is a valid integer, even if it's entered as a float (can only bet dollars, no cents, for simplification purposes)
                    elif check_float != int(check_float):
                        return render_template("apology.html", user=current_user, message="Invalid Bet. Please enter a whole number.")
                    else:
                        session['bet'] = float(check_float)  # Store the bet as a float
                except ValueError:
                    # Error
                    return render_template("apology.html", user=current_user, message="Invalid Bet. Please enter a valid number.")

                # Create a new deck every round from the API
                deck_url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
                response = requests.get(deck_url)

                # Failure from API's part, won't ever happen though
                if response.status_code != 200:
                    flash("Error: Unable to initialize deck. Please try again.", "error")
                    return redirect(url_for('views.blackjack'))
                
                # Get deck ID from the API
                deck_data = response.json()
                deck_id = deck_data['deck_id']
                session['deck_id'] = deck_id

                # Draw initial cards for player and dealer
                player_url = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=2"
                dealer_url = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=2"
                player_cards = requests.get(player_url).json()['cards']
                dealer_cards = requests.get(dealer_url).json()['cards']

                # Reset any previous session variables for the new game
                session.pop('final_player_cards', None)
                session.pop('final_dealer_cards', None)

                # Set new game session
                session['player_cards'] = player_cards
                session['dealer_cards'] = dealer_cards
                session['dealer_first_card_face_down'] = True

                session['result'] = ""  # Reset result

                # Returns the user to the game
                return redirect(url_for('views.blackjack'))
        elif deck_id:
            # Once another post request, game will have started meaning there is a deck of cards to draw from
            if action == 'hit':  # Player draws another card
                try:
                    # Request a new card for the user
                    player_url = f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1"
                    new_card_response = requests.get(player_url).json()

                    # Add the new card to the player's hand if it exists
                    if 'cards' in new_card_response and new_card_response['cards']:
                        new_card = new_card_response['cards'][0]
                        session['player_cards'].append(new_card)
                        session.modified = True

                        # Check if the player busted (hand value > 21)
                        if calculate_hand_value(session['player_cards']) > 21:
                            session['result'] = f"You busted ${session['bet']:.2f} :("
                            current_user.cash -= session['bet']  # Deduct bet from player's cash
                            db.session.commit()

                            # Copy of game just played
                            session['final_player_cards'] = session['player_cards']
                            session['final_dealer_cards'] = session['dealer_cards']

                            # Log the game result
                            add_game_stat(current_user, 'Blackjack', session['bet'], 'Lose')

                            # Clear game-related session variables
                            clear_blackjack_game()

                            # Render the game page showing the bust result
                            return render_template("blackjack.html", user=current_user,
                                                   player_cards=session.get('player_cards', []),
                                                   dealer_cards=session.get('dealer_cards', []),
                                                   result=session.get('result', ''))
                    else:
                        # Handle API failure for drawing a new card (not likely but still important)
                        return render_template("apology.html", message="We apologize for the inconvenience. It seems we encountered an issue on our end.")
                except ValueError:
                    # Invalid session data
                    return render_template("blackjack.html", user=current_user,
                                           player_cards=session.get('player_cards', []),
                                           dealer_cards=session.get('dealer_cards', []),
                                           result=session.get('result', ''))
                # Render the game page to display the updated hand
                return render_template("blackjack.html", user=current_user,
                                       player_cards=session['player_cards'],
                                       dealer_cards=session['dealer_cards'],
                                       result=session.get('result'),
                                       dealer_back_url="https://deckofcardsapi.com/static/img/back.png")
            elif action == 'stand': # User stands and ends their turn

                # Change this to show the dealers cards
                session['dealer_first_card_face_down'] = False

                # Calculate hand values for player and dealer
                player_value = calculate_hand_value(session['player_cards'])
                dealer_value = calculate_hand_value(session['dealer_cards'])

                # Simulate dealer's turn (dealer hits until value >= 17)            
                while dealer_value < 17:
                    dealer_url = f"https://deckofcardsapi.com/api/deck/{session['deck_id']}/draw/?count=1"
                    new_card = requests.get(dealer_url).json()['cards'][0]
                    session['dealer_cards'].append(new_card)
                    session.modified = True
                    dealer_value = calculate_hand_value(session['dealer_cards'])

                # Determine the result
                result = ""
                if dealer_value > 21 or player_value > dealer_value:
                    result = f"You win ${session['bet']:.2f}!!!"
                    current_user.cash += session['bet']  # Add the bet to the user's balance
                    add_game_stat(current_user, 'Blackjack', session['bet'], 'Win')
                elif player_value < dealer_value:
                    result = f"You lose ${session['bet']:.2f} :("
                    current_user.cash -= session['bet']  # Deduct the bet from user's balance
                    add_game_stat(current_user, 'Blackjack', session['bet'], 'Lose')
                else:
                    result = "It's a tie!"  # No change in cash if it's a tie
                    add_game_stat(current_user, 'Blackjack', session['bet'], 'Tie')

                # Update session result and commit all changes to database
                session['result'] = result
                db.session.commit()

                # Copy of game just played
                session['final_player_cards'] = session['player_cards']
                session['final_dealer_cards'] = session['dealer_cards']

                # Clean up the session after the game is over
                clear_blackjack_game()

                return render_template("blackjack.html", user=current_user,
            player_cards=session.get('player_cards', []),
            dealer_cards=session.get('dealer_cards', []),
            result=session.get('result', ''),
            dealer_back_url="https://deckofcardsapi.com/static/img/back.png")    
    # Render the blackjack page with session data
    return render_template(
        "blackjack.html", user=current_user,
        player_cards=session.get('player_cards', []),
        dealer_cards=session.get('dealer_cards', []),
        result=session.get('result', ''),
        dealer_back_url="https://deckofcardsapi.com/static/img/back.png"  # Add the dealer back card URL
    )

# Roulette (mainly javascript)
@views.route('/roulette')
@login_required
def roulette():
    return render_template("roulette.html", user=current_user)

# Roulette calls function to update users cash
@views.route('/update_cash', methods=['POST'])
@login_required
def update_cash():
    # Parse JSON data sent from the frontend and get value
    data = request.json 
    new_cash = data.get('new_cash')

    # Check if cash is even provided and there wasn't an error somewhere
    if new_cash:
        try:
            # Update the current user's cash in the database
            current_user.cash = new_cash
            db.session.commit()

            # Respond with success and the updated cash value
            return jsonify({'success': True, 'cash': current_user.cash}), 200
        except Exception as e:
            # Error
            return jsonify({'success': False, 'error': str(e)}), 500
    # Error because 'new_cash' is not valid
    return jsonify({'success': False, 'error': 'Invalid data'}), 400

# Another route to help assist roulette
@views.route("/update_game_stats", methods=["POST"])
@login_required
def update_game_stats():
    # Parse JSON data from the frontend
    data = request.get_json()

    # Get bet and result
    bet = data.get("bet")
    result = data.get("result")

    # Create a new GameStats entry
    add_game_stat(current_user, "Roulette", bet, result)

# FINAL GAME: SLOT MACHINE
@views.route("/slots", methods=['GET', 'POST'])
@login_required
def slots():
    # Set a dynamic cost for a single spin (1% of users cash)
    if current_user.cash >= 100:
        spin_cost = int(current_user.cash * 0.01)  # Cost is 1% of user's cash
    else: 
        spin_cost = 1  # Minimum cost of 1

    # When the slot machine is played
    if request.method == 'POST':
        # Check if the user has enough cash
        if current_user.cash < spin_cost:
            return render_template("apology.html", user=current_user, message="Can't Place Bet. You Are Too Poor.")
        else:
            # Get payout multiplier (if user won, how much of their bet did they win)
            data = request.get_json()
            payout_multiplier = data.get("payout")  # Payout multiplier

            # Calculate winnings
            winnings = spin_cost * payout_multiplier

            # If the user actually won
            if winnings > 0:
                # Update cash, commit changes, and add a new game stat
                current_user.cash += winnings
                db.session.commit()
                add_game_stat(current_user, "Slots", winnings, "Win")
            else: 
                # Otherwise, they lost
                add_game_stat(current_user, "Slots", spin_cost, "Lose")

            # Send response back to the front end
            return jsonify({
                'current_cash': current_user.cash,
                'spin_cost': spin_cost,
                'winnings': winnings,
                'payout_multiplier': payout_multiplier
            }), 200

    return render_template("slots.html", user=current_user, spin_cost=spin_cost)
