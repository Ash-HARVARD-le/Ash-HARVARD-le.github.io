from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
return "Hello, World!"

if __name__ == "__main__":
app.run(debug=True)

# import os

# from cs50 import SQL
# from flask import Flask, flash, redirect, render_template, request, session
# from flask_session import Session
# from werkzeug.security import check_password_hash, generate_password_hash

# from helpers import apology, login_required, lookup, usd

# # Configure application
# app = Flask(__name__)

# # Custom filter
# app.jinja_env.filters["usd"] = usd

# # Configure session to use filesystem (instead of signed cookies)
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

# # Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")


# @app.after_request
# def after_request(response):
#     """Ensure responses aren't cached"""
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Expires"] = 0
#     response.headers["Pragma"] = "no-cache"
#     return response


# @app.route("/")
# @login_required
# def index():
#     """Show portfolio of stocks"""

#     # Get user's portfolio/transactions
#     portfolio = db.execute(
#         "SELECT symbol, SUM(shares) FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])

#     # Get user's cash
#     cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
#     cash = cash[0]["cash"]

#     # Total stocks worth
#     stocks_worth = 0

#     # Loop through portfolio to display on index.html
#     for stock in portfolio:
#         stock_data = lookup(stock["symbol"])
#         stock["price"] = stock_data["price"]
#         stock["worth"] = stock["price"] * stock["SUM(shares)"]
#         stocks_worth += stock["worth"]

#     # Render home page
#     return render_template("index.html", portfolio=portfolio, cash=cash, stocks_worth=stocks_worth)


# @app.route("/buy", methods=["GET", "POST"])
# @login_required
# def buy():
#     """Buy shares of stock"""

#     # If post method
#     if request.method == "POST":

#         # Get input
#         symbol = request.form.get("symbol")
#         shares = request.form.get("shares")

#         # Check user input (can't be empty...
#         if not symbol:
#             return apology("Symbol IS required (Thought you were slick huh)", 400)
#         # ...or not a number, or less than 1)
#         if not shares or not shares.isdigit() or int(shares) < 1:
#             return apology("Positive digits are required (Thought you were slick huh)", 400)

#         # Lookup symbol and check if it exists
#         stock = lookup(symbol)
#         if not stock:
#             return apology("Please recheck your symbol", 400)

#         # Look up stock price and user's cash
#         cost = int(shares) * stock["price"]
#         user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
#         cash = user[0]["cash"]

#         # Buy if capable and update the user's cash and insert into transactions
#         if cash >= cost:
#             db.execute("INSERT INTO transactions (user_id, symbol, stock, shares, share_price, cost) VALUES(?, ?, ?, ?, ?, ?)",
#                        session["user_id"], symbol, stock["name"], int(shares), stock["price"], cost)
#             db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - cost, session["user_id"])
#             flash("Bought!")
#             return redirect("/")
#         else:
#             # Can't afford
#             return apology("You are poor. Sorry.", 400)
#     else:
#         # When get method
#         return render_template("buy.html")


# @app.route("/history")
# @login_required
# def history():
#     """Show history of transactions"""

#     # Print elements of all user transactions to history.html
#     portfolio = db.execute(
#         "SELECT symbol, stock, shares, share_price, time FROM transactions WHERE user_id = ? ORDER BY time DESC", session["user_id"])
#     return render_template("history.html", portfolio=portfolio)


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     """Log user in"""

#     # Forget any user_id
#     session.clear()

#     # User reached route via POST (as by submitting a form via POST)
#     if request.method == "POST":
#         # Ensure username was submitted
#         if not request.form.get("username"):
#             return apology("must provide username", 403)

#         # Ensure password was submitted
#         elif not request.form.get("password"):
#             return apology("must provide password", 403)

#         # Query database for username
#         rows = db.execute(
#             "SELECT * FROM users WHERE username = ?", request.form.get("username")
#         )

#         # Ensure username exists and password is correct
#         if len(rows) != 1 or not check_password_hash(
#             rows[0]["hash"], request.form.get("password")
#         ):
#             return apology("invalid username and/or password", 403)

#         # Remember which user has logged in
#         session["user_id"] = rows[0]["id"]

#         # Redirect user to home page
#         return redirect("/")

#     # User reached route via GET (as by clicking a link or via redirect)
#     else:
#         return render_template("login.html")


# @app.route("/logout")
# def logout():
#     """Log user out"""

#     # Forget any user_id
#     session.clear()

#     # Redirect user to login form
#     return redirect("/")


# @app.route("/quote", methods=["GET", "POST"])
# @login_required
# def quote():
#     """Get stock quote."""

#     # If post method
#     if request.method == "POST":

#         # Get user input and check validity
#         symbol = request.form.get("symbol")
#         if not symbol:
#             return apology("Symbol IS required (Thought you were slick huh)", 400)

#         # Lookup symbol and check if it exists
#         stock = lookup(symbol)
#         if stock:
#             # If all's well, display this stock in quoted.html
#             return render_template("quoted.html", symbol=stock)
#         else:
#             return apology("Please recheck your symbol", 400)

#     else:
#         # Get method
#         return render_template("quote.html")


# @app.route("/register", methods=["GET", "POST"])
# def register():
#     """Register user"""

#     # If post method
#     if request.method == "POST":

#         # Get all user input
#         username = request.form.get("username")
#         password = request.form.get("password")
#         confirmation = request.form.get("confirmation")

#         # Check if anything was left blank
#         if not username:
#             return apology("Username IS required (Thought you were slick huh)", 400)
#         if not password or not confirmation:
#             return apology("Password IS required (Thought you were slick huh)", 400)

#         # Check if passwords match
#         if password != confirmation:
#             return apology("Passwords do not match", 400)

#         # Check if username already exists and INSERT if not
#         try:
#             db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
#                        username, generate_password_hash(password))
#             flash("Registered!")
#         except ValueError:
#             return apology("Sorry! Username already exists :(", 400)

#         # At this point, everything should be accounted for and go to login for a valid register
#         return redirect("/login")

#     else:
#         # Get method
#         return render_template("register.html")


# @app.route("/sell", methods=["GET", "POST"])
# @login_required
# def sell():
#     """Sell shares of stock"""

#     # If post method
#     if request.method == "POST":

#         # Get ALL user input / check for validity
#         symbol = request.form.get("symbol")
#         if not symbol:
#             return apology("Symbol IS required (Thought you were slick huh)", 400)
#         stock = lookup(symbol)
#         if not stock:
#             return apology("Please recheck your symbol", 400)
#         sold_shares = request.form.get("shares")
#         if not sold_shares or not sold_shares.isdigit() or int(sold_shares) < 1:
#             return apology("Positive digits are required (Thought you were slick huh)", 400)

#         # Sell shares if user has enough valid shares
#         # Get transaction portfolio on the current user and the symbol they want to sell | Also get their cash to update it later
#         portfolio = db.execute(
#             "SELECT SUM(shares) FROM transactions WHERE user_id = ? AND symbol = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"], symbol)
#         cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])

#         # If user has enough shares to sell then...
#         if portfolio[0]["SUM(shares)"] >= int(sold_shares):
#             # Update user's cash and insert this into transactions
#             profit = stock["price"] * int(sold_shares)
#             db.execute("UPDATE users SET cash = ? WHERE id = ?",
#                        cash[0]["cash"] + profit, session["user_id"])
#             db.execute("INSERT INTO transactions (user_id, symbol, stock, shares, share_price, cost) VALUES(?, ?, ?, ?, ?, ?)",
#                        session["user_id"], symbol, stock["name"], -int(sold_shares), stock["price"], profit)
#             flash("Sold!")
#             return redirect("/")
#         else:
#             # Otherwise, user does not own enough shares to sell
#             return apology("You don't own enough shares", 400)

#     else:
#         # Get method needs to display all the symbols for dropdown options
#         portfolio = db.execute(
#             "SELECT symbol FROM transactions WHERE user_id = ? GROUP BY symbol HAVING SUM(shares) > 0", session["user_id"])
#         return render_template("sell.html", portfolio=portfolio)


# @app.route("/account")
# @login_required
# def account():
#     """Show user account information"""

#     # Get user's username and render it into the user's account page
#     username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
#     return render_template("account.html", username=username[0]["username"])


# @app.route("/updatepassword", methods=["GET", "POST"])
# @login_required
# def updatepassword():
#     """Update User Password (only when logged in, and no 'Forgot Password?' because I would need two-step verification)"""

#     # If post method
#     if request.method == "POST":

#         # Get all user input
#         username = request.form.get("username")
#         old_password = request.form.get("old_password")
#         new_password = request.form.get("new_password")
#         confirmation = request.form.get("confirmation")

#         # Check if anything was left blank
#         if not username:
#             return apology("Username IS required (Thought you were slick huh)", 400)
#         if not old_password or not new_password or not confirmation:
#             return apology("Password IS required (Thought you were slick huh)", 400)

#         # Check if passwords match
#         if new_password != confirmation:
#             return apology("Passwords do not match", 400)

#         # Check if username and old password match records
#         user = db.execute("SELECT username, hash FROM users WHERE id = ?", session["user_id"])
#         records_username = user[0]["username"]
#         records_password = user[0]["hash"]

#         if username != records_username:
#             return apology("Wrong username!", 400)
#         if not check_password_hash(records_password, old_password):
#             return apology("Wrong old password!", 400)

#         # If all is well, and there were no mistakes, the password should be updated for this user
#         db.execute("UPDATE users SET hash = ? WHERE id = ?",
#                    generate_password_hash(new_password), session["user_id"])
#         flash("Updated Password!")

#         # At this point, everything should be accounted for and go to login to sign in again
#         return redirect("/login")

#     else:
#         # Get method
#         return render_template("updatepassword.html")
