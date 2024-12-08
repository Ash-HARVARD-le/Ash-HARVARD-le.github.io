from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import User, Deposit, GameStats
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .helpers import validate_credit_card, clear_blackjack_session

# Define auth blueprint, this is for more sensitive pages
auth = Blueprint('auth', __name__)

# USER LOGIN!!!
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login functionality. 
    Validates the username and password, logs the user in if valid, or returns appropriate errors.
    """

    if request.method == 'POST':
        # Get the username and password from the login form
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database for the user by username
        user = User.query.filter_by(username=username).first()
        if user:
            # Check if user exists and then if the provided password matches the stored hash
            if check_password_hash(user.password, password):
                # Greets users with a message saying they have claimed $100 MALANION DOLLARS 🤑🤑🤑 and they gain access to all features of website
                flash('You have claimed your 100 Malanion dollars! Start gambling and win to prove you\'re not addicted, but just working.')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                # Wrong password
                return render_template("apology.html", user=current_user, message = "Incorrect Password")
        else:
            # Wrong user
            return render_template("apology.html", user=current_user, message = "User does not exist")
    else:
        # If they GET on the page then just render the page
        return render_template("login.html", user=current_user)

# LOGOUT USER, only accessible if logged in
@auth.route('/logout')
@login_required
def logout():
    # Clears game session, logs user out, and redirects to login page
    clear_blackjack_session()
    logout_user()
    return redirect(url_for('auth.login'))

# REGISTER A USER
@auth.route('/register', methods=['GET', 'POST'])
def register():
    # When registering an account
    if request.method == 'POST':
        # Get user info
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        # Ensure username is not taken
        user = User.query.filter_by(username=username).first()
        if user:
            return render_template("apology.html", user=current_user, message = "User already exists")
        if not username:
            # No username provided
            return render_template("apology.html", user=current_user, message = "Invalid Username (Thought you were slick huh)")
        if not password or not confirmation:
            # Bad passwords
            return render_template("apology.html", user=current_user, message = "Invalid Password (Thought you were slick huh)")
        if password != confirmation:
            return render_template("apology.html", user=current_user, message = "Passwords do not match")
        
        # Register user into the User database, store their id, username, password (hashed), and commit changes
        new_user = User(username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))
        db.session.add(new_user)
        db.session.commit()

        # When successfully registered, they get a message about receiving an incentive for registering, and are redirected towards login page
        flash("Thank you for registering! As a gift, you have received 100 Malanion dollars! Log in to claim your reward!")
        return redirect(url_for('auth.login'))
    else:
        # Otherwise, just render the register template
        return render_template("register.html", user=current_user)
    
# SENSITIVE ACCOUNT PAGE
@auth.route('/account')
@login_required
def account():
    # Lead user towards the account page
    return render_template("account.html", user=current_user)

# DELETE USER ACCOUNT
@auth.route('/delete', methods=['POST'])
@login_required
def delete_account():
    # Deletes everything related to the user and commits changes
    Deposit.query.filter_by(user_id=current_user.id).delete()
    GameStats.query.filter_by(user_id=current_user.id).delete()
    db.session.delete(current_user)
    db.session.commit()

    # Clear games and log out
    clear_blackjack_session()
    logout_user()

    # Message saying account was deleted and goes back to login
    flash('Your account has been deleted successfully.')
    return redirect(url_for('auth.login'))

# UPDATE USER PASSWORD
@auth.route("/update_password", methods=["GET", "POST"])
@login_required
def update_password():
    # If user wants to update password
    if request.method == "POST":
        # Get user input
        username = request.form.get("username")
        old_password = request.form.get("old_password")
        new_password = request.form.get("new_password")
        confirmation = request.form.get("confirmation")

        # Check any bad input
        if not username:
            return render_template("apology.html", user=current_user, message = "Invalid Username")
        if not old_password or not new_password or not confirmation:
            return render_template("apology.html", user=current_user, message = "Invalid Password(s)")
        
        # Bad password input
        if new_password != confirmation:
            return render_template("apology.html", user=current_user, message = "Passwords do not match")
        
        # Check if user even exists, and if they provided the right information to update their password
        if not current_user:
            return render_template("apology.html", user=current_user, message = "User does not exist")
        if username != current_user.username:
            return render_template("apology.html", user=current_user, message = "You cannot update this account")
        if not check_password_hash(current_user.password, old_password):
            return render_template("apology.html", user=current_user, message = "Wrong old password!")
        
        # If all successful, proceed with changing password and commit the change
        current_user.password = generate_password_hash(new_password)
        db.session.commit()

        # Logs out user, message for success, and they have to log in again
        logout_user()
        flash("Updated Password!")
        return redirect("/login")
    else:
        # Render the update password page
        return render_template("update_password.html", user=current_user)
    
# DEPOSIT CASH WITH HUID
@auth.route('/huid-deposit', methods=['POST'])
@login_required
def huid_deposit():
    # Get the deposit amount from the form
    amount = request.form.get('huid-amount')
    huid = request.form.get('huid')

    # Ensure valid amount input (limit to $1,000, otherwise it's too much money)
    try:
        amount = float(amount)
        if amount <= 0 or amount > 1000:
            return render_template("apology.html", user=current_user, message = "Invalid Amount (must be within $0.01 - $1,000)")
    except ValueError:
        return render_template("apology.html", user=current_user, message = "Invalid Amount (must be a VALID value between $0.01 - $1,000)")
    
    # Check valid HUID input
    if not huid or not huid.isdigit() or len(huid) != 8:
        return render_template("apology.html", user=current_user, message = "Invalid HUID! (MUST be 8 NUMBERS long)")
    
    # If the user's HUID is locked, check if the entered HUID matches the stored one
    # User can't change their HUID so once it's locked then this is the HUID they "take from," obviously not real money
    if current_user.huid_locked:
        if current_user.huid != huid:
            return render_template("apology.html", user=current_user, message="Incorrect HUID! You cannot deposit with a different HUID.")
    else:
        # If HUID is not locked (first time depositing with huid), store the HUID and lock it
        current_user.huid = huid
        current_user.huid_locked = True
    
    # Update users cash
    current_user.cash = current_user.cash + float(amount)
    db.session.commit()

    # Create a new deposit record
    new_deposit = Deposit(user_id=current_user.id, amount=float(amount), deposit_type="Crimson Cash")
    db.session.add(new_deposit)
    db.session.commit()

    # Success message (goes back to account page where they can view their cash balance)
    flash(f'Successfully deposited ${amount} through Crimson Cash!')
    return redirect(url_for('auth.account'))

# NOT RECOMMENDED TO USE, but still here because I thought it would be funny
@auth.route('/credit-deposit', methods=['POST'])
@login_required
def credit_deposit():
    # Gets credit card info and amount
    card_number = request.form.get('credit-card-number')
    expiration_date = request.form.get('expiration-date')
    cvv = request.form.get('cvv')
    amount = request.form.get('credit-amount')

    # Validate the input
    try:
        amount = float(amount)
        if amount <= 0 or amount > 10000:
            return render_template("apology.html", user=current_user, message="Invalid Amount (Must be within $0.01 - $10,000)")
    except ValueError:
        return render_template("apology.html", user=current_user, message="Invalid Amount (Must be a VALID value between $0.01 - $10,000)")
    
    # Check validity of credit card number
    if not card_number or not card_number.isdigit() or len(card_number) > 16 or len(card_number) < 13 or not validate_credit_card(card_number):
        return render_template("apology.html", user=current_user, message="Invalid Credit Card Number")
    
    # No real check for expiration date (how would I know it's right) other than a valid input in valid format 
    if not expiration_date or len(expiration_date) != 5 or expiration_date[2] != '/' or not expiration_date[:2].isdigit() or not expiration_date[3:].isdigit():
        return render_template("apology.html", user=current_user, message="Invalid Expiration Date! Use the Format: MM/YY")
    
    # Validate the expiration DATE
    month = int(expiration_date[:2])
    year = int(expiration_date[3:])
    if month < 1 or month > 12:
        return render_template("apology.html", user=current_user, message="Invalid Month! (Must be between 01 - 12)")
    if year < 0 or year > 99:
        return render_template("apology.html", user=current_user, message="Invalid Year! (Must be within 00 - 99)")
    
    # Validate cvv
    if not cvv or len(cvv) > 4 or len(cvv) < 3 or not cvv.isdigit():
        return render_template("apology.html", user=current_user, message="Invalid CVV!")
    
    # If ALL successful, then update the users cash and commit changes
    current_user.cash += amount
    db.session.commit()

    # Store the deposit in the database
    # USERS ARE NOT RECOMMENDED TO ACTUALLY USE THIS FEATURE, but it was a cool feature to add
    # Users can put in a fake expiration date, cvv, and credit card number (Week 1: David's Visa: 4003600000000014)
    new_deposit = Deposit(
        user_id=current_user.id,
        amount=amount,
        deposit_type="Credit Card",
        credit_card=card_number,
        exp_date=expiration_date,
        cvv=cvv
    )
    db.session.add(new_deposit)
    db.session.commit()

    # Success and redirect to account to see money
    flash(f'Successfully deposited ${amount} using Credit Card!')
    return redirect(url_for('auth.account'))
