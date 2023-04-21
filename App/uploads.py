from flask import Flask, Blueprint, render_template, flash, request, session
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os
import uuid
from .models import Product
from . import db

uploads = Blueprint("upload", __name__)

app = Flask(__name__)
app.config["UPLOAD_DIRECTORY"] = "App/static/images"
app.config["ALLOWED_EXTENSIONS"] = [".jpg", ".jpeg", ".png", ".gif"]
app.config["MAX_CONTENT_LENGTH"] = 5*1024*1024
app.config["SESSION_PERMANENT"] = False


@uploads.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    session.clear()
    products = Product.query.filter_by(product_owner=current_user.id).order_by(Product.product_id.desc())\
    .all()
    if request.method == "POST":
        product_name = request.form.get("product_name")
        description = request.form.get("description")
        price = request.form.get("price")
        image = request.files["image"]
        filename = str(uuid.uuid1())+os.path.splitext(image.filename)[1]
        extension = os.path.splitext(image.filename)[1].lower()
        try:
            if extension in app.config["ALLOWED_EXTENSIONS"]:
                image.save(os.path.join(app.config["UPLOAD_DIRECTORY"], secure_filename(filename)))
                product_owner = current_user.id
                new_product = Product(product_name=product_name, description=description, price=price,
                                      filename=filename, product_owner=product_owner)
                db.session.add(new_product)
                db.session.commit()
                flash("Your product have been added successfully", category="success")
                products = Product.query.filter_by(product_owner=product_owner).order_by(Product.product_id.desc())\
                    .all()
                return render_template("add.html", products=products, trader=current_user)
            else:
                flash("The file you are tyring to upload is not a picture !!", category="error")
        except RequestEntityTooLarge:
            flash("The file your are uploading is too large, please upload a picture !! ", category="error")

    return render_template("add.html", trader=current_user, products=products)
