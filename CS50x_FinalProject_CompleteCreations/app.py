import os

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from flask_mail import Mail, Message
import time

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_USERNAME"] = 'my email (taken out for privacy purposes in this assignment)'
app.config["MAIL_PASSWORD"] = 'my email password (taken out for privacy purposes in this assignment)'
Session(app)
mail = Mail(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "GET":
        flash("")
        return render_template("contact.html")
    else:
        flash("")
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("text")

        if (name == None or name == "" or name == " "):
            flash("Please Enter Your Name")
            return render_template("contact.html")
        elif(not(' ' in name)):
            flash("Please Enter Your First and Last Name")
            return render_template("contact.html")
        elif(message == None or message == "" or message == " "):
            flash("Please Enter Your Order Details")
            return render_template("contact.html")

        try:
            msg = Message("Order Request", sender = email, recipients = ['chriscomp2001@gmail.com'])
            msg.body = message
            mail.send(msg)
            flash("Thank You For Your Order Request! [Owner] Will Be In Touch :)")
            return render_template("contact.html")
        except:
            flash("Please Enter A Valid Email Address")
            return render_template("contact.html")

@app.route("/projects", methods=["GET", "POST"])
def projects():
    if request.method == "GET":
        return render_template("projects.html")
    else:
        return render_template("projects.html")

@app.route("/about", methods=["GET", "POST"])
def about():
    if request.method == "GET":
        return render_template("about.html")
    else:
        return render_template("about.html")


