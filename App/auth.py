from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Trader, Post
from werkzeug.security import check_password_hash
from flask_login import login_user, current_user, login_required
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not request.form["email"] or not request.form["password"]:
            flash("All fields are required !!", category="error")
        else:
            email = request.form.get("email")
            password = request.form.get("password")
            trader = Trader.query.filter_by(email=email).first()
            if trader:
                if check_password_hash(trader.password, password):
                    login_user(trader, remember=True)
                    return redirect(url_for("views.home"))
                else:
                    flash("Incorrect password,please try again", category="error")
            else:
                flash("You do not have an account!! please sign-up to create one", category="error")
    return render_template("login.html", trader=current_user)


@auth.route("/view_post")
@login_required
def view_post():
    posts = Post.query.order_by(Post.post_id.desc()).all()
    return render_template("view_post.html", trader=current_user, posts=posts)


@auth.route("/delete_post/<post_id>")
@login_required
def delete_post(post_id):
    search_post = Post.query.filter_by(post_id=post_id).first()
    if search_post:
        db.session.delete(search_post)
        db.session.commit()
        flash("The backorder have been deleted successfully", category="success")
        return redirect(url_for("auth.view_post"))
    else:
        flash("The backorder does not exist", category="error")
