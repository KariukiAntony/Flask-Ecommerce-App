from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import re
from .models import Trader, Product, Post
from werkzeug.security import generate_password_hash
from . import db
from flask_login import current_user, login_required, logout_user

views = Blueprint("views", __name__)


@views.route("/")
def index():
    return render_template("index.html")


@views.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        session.clear()
        if not request.form["email"] or not request.form["phone"] or not request.form["username"] \
                or not request.form["password"] or not request.form["confirm"]:
            flash("All fields are required !!!", category="error")
        else:
            email = request.form.get("email")
            phone_number = request.form.get("phone")
            username = request.form.get("username")
            password = request.form.get("password")
            confirm = request.form.get("confirm")
            correct_email = '^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
            if re.search(correct_email, email):
                if re.match("^(07|01)\d{8}$", phone_number):
                    if len(username) > 3:
                        if len(password) > 6:
                            if password == confirm:
                                found_email = Trader.query.filter_by(email=email).first()
                                hashed_password = generate_password_hash(password)
                                if found_email:
                                    flash("The email already exists !!", category="error")
                                else:
                                    new_trader = Trader(email=email, phone_number=phone_number, username=username,
                                                        password=hashed_password)
                                    db.session.add(new_trader)
                                    db.session.commit()
                                    flash("Account created successfully", category="success")
                                    return redirect(url_for("auth.login"))
                            else:
                                flash("The passwords do not match !!", category="error")
                        else:
                            flash("Password must be at least 6 characters !!", category="error")
                    else:
                        flash("Your username is too short", category="error")
                else:
                    flash("Invalid phone number. Please enter a valid phone number!!", category="error")
            else:
                flash("Invalid email !!, please enter a valid email", category="error")

    return render_template("sign-up.html", trader=current_user)


@views.route("/home")
@login_required
def home():
    products = Product.query.order_by(Product.product_id.desc()).all()
    return render_template("home.html", trader=current_user, products=products)


@views.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        post = request.form.get("post")
        author = current_user.id
        phone_number = current_user.phone_number
        if post:
            new_post = Post(post=post, phone_number=phone_number, post_author=author)
            db.session.add(new_post)
            db.session.commit()
            flash("The order have been posted successfully", category="success")
        else:
            flash("The order cannot be empty !!", category="error")
    return render_template("post.html", trader=current_user)


@views.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
