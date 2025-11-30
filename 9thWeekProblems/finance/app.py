import os
from datetime import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd


# Initialize Flask application
app = Flask(__name__)

# Set secret key for session encryption (uses environment variable or fallback)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

# Register custom Jinja filter for USD formatting
app.jinja_env.filters["usd"] = usd

# Configure session storage to use filesystem instead of cookies
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize database connection
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """
    Disable caching for all responses to ensure users see fresh data.
    This prevents browsers from storing outdated stock prices or portfolio values.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """
    Display the user's portfolio homepage showing all owned stocks,
    current prices, and total portfolio value.
    """
    user_id = session.get("user_id")
    
    # Fetch user's stocks and account information
    try:
        stocks = db.execute(
            "SELECT * FROM user_shares WHERE user = ? AND quantity > 0", 
            user_id
        )
        user_rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
        
        if not user_rows:
            return apology("Could not find user.", 403)
        
        user = user_rows[0]
        user["stock_values"] = 0
    except Exception as error:
        return apology(f"Could not fetch the data. {error}", 500)

    # Build stock price cache and compute portfolio value
    stock_data = {}
    total_portfolio_value = 0
    
    for stock in stocks:
        symbol = stock["symbol"]
        
        # Cache stock price lookup to avoid redundant API calls
        if symbol not in stock_data:
            price_info = lookup(symbol)
            if price_info:
                stock_data[symbol] = price_info
        
        # Accumulate total portfolio value
        if symbol in stock_data:
            holding_value = stock["quantity"] * stock_data[symbol]["price"]
            total_portfolio_value += holding_value
    
    user["stock_values"] = total_portfolio_value

    return render_template("index.html", stocks=stocks, user=user, stock_data=stock_data)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """
    Handle stock purchase requests.
    GET: Display the buy form
    POST: Process the purchase transaction
    """
    if request.method == "GET":
        return render_template("buy.html")
    
    # Extract and sanitize form data
    symbol = request.form.get("symbol", "").strip()
    shares_input = request.form.get("shares", "").strip()
    
    # Parse and validate quantity
    try:
        quantity = int(shares_input)
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
    except (ValueError, TypeError):
        return apology("Enter positive integer for number of shares.")
    
    # Fetch current market price
    try:
        stock_data = lookup(symbol)
    except Exception as error:
        return apology(f"Error: {error}.", 400)

    if not stock_data:
        return apology("Invalid symbol.", 400)

    # Compute transaction cost
    transaction_cost = quantity * stock_data["price"]
    current_user_id = session.get("user_id")

    # Retrieve user account details
    user_rows = db.execute("SELECT * FROM users WHERE id = ?", current_user_id)
    if not user_rows:
        return apology("Could not find the user.", 403)
    
    user = user_rows[0]
    available_cash = user.get("cash")
    
    # Check if user can afford the purchase
    if transaction_cost > available_cash:
        return apology("Not enough money to buy, you brook.")

    # Process transaction in database
    try:
        new_cash_balance = available_cash - transaction_cost
        
        # Record new share ownership
        db.execute(
            "INSERT INTO user_shares (user, symbol, price, quantity) VALUES(?, ?, ?, ?)", 
            current_user_id, symbol, stock_data["price"], quantity
        )
        
        # Update user's cash balance
        db.execute(
            "UPDATE users SET cash = ? WHERE id = ?", 
            new_cash_balance, current_user_id
        )
        
        # Log transaction to history
        db.execute(
            "INSERT INTO user_histories (user, symbol, buying_price, activity, quantity) VALUES(?, ?, ?, ?, ?)", 
            current_user_id, symbol, stock_data["price"], 'buy', quantity
        )
    except Exception as error:
        return apology(f"Couldn't buy the stock. {error}")

    return redirect("/")


@app.route("/history")
@login_required
def history():
    """
    Display complete transaction history for the logged-in user,
    including all buy and sell activities.
    """
    user_id = session.get("user_id")
    
    # Verify user exists
    user_rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if len(user_rows) != 1:
        return apology("Could not find the user.", 403)
    user = user_rows[0]

    # Fetch all transaction records
    histories = db.execute("SELECT * FROM user_histories WHERE user = ?", user_id)
    
    return render_template("history.html", histories=histories)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Authenticate user login.
    GET: Display login form
    POST: Validate credentials and create session
    """
    # Clear any existing session data
    session.clear()

    if request.method == "POST":
        # Extract credentials from form
        username_input = request.form.get("username")
        password_input = request.form.get("password")
        
        # Validate username input
        if not username_input:
            return apology("must provide username", 403)

        # Validate password input
        if not password_input:
            return apology("must provide password", 403)

        # Search for user account
        user_records = db.execute(
            "SELECT * FROM users WHERE username = ?", 
            username_input
        )

        # Authenticate credentials
        is_valid_user = (
            len(user_records) == 1 and 
            check_password_hash(user_records[0]["hash"], password_input)
        )
        
        if not is_valid_user:
            return apology("invalid username and/or password", 403)

        # Establish user session
        session["user_id"] = user_records[0]["id"]

        # Redirect to portfolio homepage
        return redirect("/")

    # Display login form for GET requests
    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Log out the current user by clearing their session data
    and redirecting to the login page.
    """
    # Clear all session data
    session.clear()

    # Redirect to login page
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """
    Look up current stock price by symbol.
    GET: Display quote lookup form
    POST: Fetch and display stock information
    """
    if request.method == "GET":
        return render_template("quote.html")
    
    # Validate symbol input
    symbol = request.form.get("symbol", "")
    if not symbol:
        return apology("Provide valid symbol.", 400)
    
    # Lookup stock information
    try:
        data = lookup(symbol)
    except Exception as error:
        return apology(f"ERROR: {error}", 500)
    
    if not data:
        return apology("Code does not exist", 400)
    
    return render_template("quote.html", data=data)



@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register a new user account.
    GET: Display registration form
    POST: Create new user and log them in
    """
    if request.method == "GET":
        return render_template('register_user.html')
    
    # Extract and sanitize registration form data
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    confirm = request.form.get("confirmation", "").strip()

    # Perform input validation checks
    validation_errors = []
    
    if not username:
        return apology("must provide username", 400)
    
    if not password:
        return apology("must provide password", 400)
    
    if not confirm or confirm != password:
        return apology("confirm password must match with password", 400)

    # Verify username availability
    existing_users = db.execute("SELECT * FROM users WHERE username = ?", username)
    if existing_users:
        return apology("Username already exists.", 400)

    try:
        # Hash password for secure storage
        password_hash = generate_password_hash(password)
        
        # Insert new user record
        db.execute(
            "INSERT INTO users (username, hash) VALUES(?, ?)", 
            username, password_hash
        )

        # Fetch newly created user account
        new_user = db.execute("SELECT id FROM users WHERE username = ?", username)
        if not new_user:
            return apology("registration failed", 500)

        # Auto-login: establish session for new user
        session["user_id"] = new_user[0]["id"]
    except Exception as e:
        return apology(f"registration error: {e}", 500)

    return redirect("/")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """
    Handle stock selling transactions.
    GET: Display sell form with user's current holdings
    POST: Process the sale using FIFO (First In, First Out) method
    """
    user_id = session.get("user_id")
    
    # Retrieve user account information
    user_rows = db.execute("SELECT * FROM users WHERE id = ?", user_id)
    if not user_rows:
        return apology("Could not find user in database.", 403)
    user = user_rows[0]
    
    # Query user's active stock positions
    share_list = db.execute(
        "SELECT * FROM user_shares WHERE user = ? AND quantity > 0", 
        user_id
    )
    
    # Build price lookup cache for portfolio
    stock_data = {}
    for stock in share_list:
        symbol = stock["symbol"]
        if symbol not in stock_data:
            price_info = lookup(symbol)
            if price_info:
                stock_data[symbol] = price_info

    if request.method == "GET":
        return render_template("sell.html", stock_data=stock_data, share_list=share_list)
    
    # Extract sale parameters from form
    share_symbol = request.form.get("symbol", "")
    shares_to_sell_input = request.form.get("shares", "")
    
    # Parse and validate sell quantity
    try:
        shares_to_sell = int(shares_to_sell_input)
        if shares_to_sell <= 0:
            raise ValueError("Shares must be positive integer.")
    except (ValueError, TypeError) as error:
        return apology(f"Error: Invalid share count {error}", 400)

    # Retrieve purchase history for this stock (FIFO order)
    purchase_batches = db.execute(
        "SELECT * FROM user_shares WHERE user = ? AND symbol = ? AND quantity > 0 ORDER BY created_at", 
        user_id, share_symbol
    )
    
    if not purchase_batches:
        return apology("This share doesn't exists", 404)

    # Fetch current market price
    market_data = lookup(share_symbol)
    current_market_price = market_data["price"]
    
    # Calculate total available shares for this symbol
    total_owned = db.execute(
        "SELECT SUM(quantity) as count FROM user_shares WHERE user = ? AND symbol = ? AND quantity > 0", 
        user_id, share_symbol
    )[0]['count']
    
    # Ensure sufficient shares available
    if total_owned < shares_to_sell:
        return apology("Error: Not enough share to sell.", 400)
    
    total_proceeds = 0
    remaining_to_sell = shares_to_sell
    
    # Execute FIFO sale algorithm
    for batch in purchase_batches:
        if remaining_to_sell <= 0:
            break
        
        batch_id = batch["id"]
        batch_quantity = batch["quantity"]
        
        # Calculate shares to sell from this batch
        shares_from_batch = min(batch_quantity, remaining_to_sell)
        transaction_timestamp = datetime.now()
        
        # Update batch inventory
        db.execute(
            "UPDATE user_shares SET quantity = ?, sold_quantity = ?, updated_at = ? WHERE id = ?", 
            batch_quantity - shares_from_batch, shares_from_batch, transaction_timestamp, batch_id
        )
        
        # Log sale transaction
        db.execute(
            "INSERT INTO user_histories (user, symbol, buying_price, selling_price, activity, quantity) VALUES(?, ?, ?, ?, ?, ?)", 
            user_id, share_symbol, batch["price"], current_market_price, 'sell', shares_from_batch
        )
        
        # Accumulate sale proceeds
        batch_proceeds = current_market_price * shares_from_batch
        total_proceeds += batch_proceeds
        remaining_to_sell -= shares_from_batch

    # Credit proceeds to user account
    updated_balance = user["cash"] + total_proceeds
    db.execute(
        "UPDATE users SET cash = ? WHERE id = ?", 
        updated_balance, user_id
    )

    return redirect("/")
