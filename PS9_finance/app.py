import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    purchases = db.execute(
        "SELECT symbol, name, SUM(shares) AS sharesTotal, price FROM purchases WHERE username = ? GROUP BY symbol",
        session["user_id"],
    )

    current_cash = db.execute(
        "SELECT cash FROM users WHERE id = ?", session["user_id"]
    )[0]["cash"]

    total = 0

    for purchase in purchases:
        price = float(purchase["price"])
        total += price * int(purchase["sharesTotal"])

    return render_template(
        "index.html", purchases=purchases, cash=current_cash, usd=usd, total=total
    )


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("Shares must be an integer")

        if shares < 1 or shares == None:
            return apology("Number of Shares Does Not Exist")

        try:
            name = lookup(symbol)["name"]
            real_symbol = lookup(symbol)["symbol"]
            price = lookup(symbol)["price"]
            total = float("{:.2f}".format(price)) * shares

        except:
            return apology("Symbol Does Not Exist")

        current_cash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"]
        )[0]["cash"]

        if total > current_cash:
            return apology("Not Enough Cash")
        else:
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                current_cash - total,
                session["user_id"],
            )

            db.execute(
                "INSERT INTO purchases (date, username, symbol, shares, price, name, type) VALUES(CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?)",
                session["user_id"],
                real_symbol,
                shares,
                price,
                name,
                "Bought",
            )

        return redirect("/")


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""
    if request.method == "POST":
        if "clear" in request.form:
            purchases = {}
        else:
            purchases = db.execute(
                "SELECT * FROM purchases WHERE username = ?", session["user_id"]
            )
    else:
        purchases = db.execute(
            "SELECT * FROM purchases WHERE username = ?", session["user_id"]
        )

    return render_template("history.html", purchases=purchases)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 200)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 200)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 200)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")

        try:
            name = lookup(symbol)["name"]
            real_symbol = lookup(symbol)["symbol"]
            price = lookup(symbol)["price"]
            return render_template(
                "quoted.html", name=name, symbol=real_symbol, price=int(price), usd=usd
            )
        except:
            return apology("Symbol Does Not Exist")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        if request.form.get("username") == "":
            return apology("No Username Found")

        elif request.form.get("password") == "":
            return apology("No Password Found")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords Don't Match")

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        if len(rows) != 0:
            return apology("Username Taken")

        username = request.form.get("username")
        password = request.form.get("password")
        hash = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)", username, hash
            )
            return redirect("/")
        except:
            return apology("Username Taken")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        stocks = db.execute(
            "SELECT symbol FROM purchases  WHERE username = ? GROUP BY symbol",
            session["user_id"],
        )

        symbols = []

        for stock in stocks:
            symbols.append(stock["symbol"])

        return render_template("sell.html", symbols=symbols)
    else:
        stocks = db.execute(
            "SELECT symbol FROM purchases  WHERE username = ? GROUP BY symbol HAVING SUM(shares) > 0",
            session["user_id"],
        )

        symbols = []

        for stock in stocks:
            symbols.append(stock["symbol"])

        if request.form.get("symbol") in symbols == False:
            return apology("Select Stock You Own")
        else:
            selectedSymbol = request.form.get("symbol")

        selectedShares = db.execute(
            "SELECT SUM(shares) AS selectedS FROM purchases WHERE username = ? AND symbol = ? GROUP BY symbol",
            session["user_id"],
            selectedSymbol,
        )

        if (
            int(request.form.get("shares")) < 1
            or request.form.get("shares") == None
            or int(request.form.get("shares")) > int(selectedShares[0]["selectedS"])
        ):
            return apology("You don't own that many!")
        else:
            sharesSold = request.form.get("shares")

            purchases = db.execute(
                "SELECT symbol, name, (SUM(shares) - ?) AS sharesTotal, price AS price FROM purchases WHERE username = ? GROUP BY symbol",
                sharesSold,
                session["user_id"],
            )

            current_cash = db.execute(
                "SELECT cash FROM users WHERE id = ?", session["user_id"]
            )[0]["cash"]

            total = 0

            for purchase in purchases:
                price = float(purchase["price"])
                total += price * int(purchase["sharesTotal"])

            current_cash = db.execute(
                "SELECT cash FROM users WHERE id = ?", session["user_id"]
            )[0]["cash"]

            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?",
                current_cash + (lookup(selectedSymbol)["price"] * int(sharesSold)),
                session["user_id"],
            )

            db.execute(
                "INSERT INTO purchases (date, username, symbol, shares, price, name, type) VALUES(CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?)",
                session["user_id"],
                selectedSymbol,
                int(sharesSold) * -1,
                price,
                lookup(selectedSymbol)["name"],
                "Sold",
            )

            return redirect("/")
