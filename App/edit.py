from flask import Blueprint, request, flash, redirect, url_for, Flask
from .models import Product
from . import db
import os
from flask_login import current_user, login_required

edit = Blueprint("edit", __name__)
app = Flask(__name__)
app.config["UPLOAD_DIRECTORY"] = "App/static/images"


@edit.route("/editing/<product_id>", methods=["GET", "POST"])
@login_required
def editing(product_id):
    if request.method == "POST":
        main_product = Product.query.filter_by(product_id=product_id).first()
        if main_product.product_owner != current_user.id:
            flash("Your are not allowed to edit this product!!!", category="error")
        if main_product:
            main_product.product_name = request.form.get("new_name")
            main_product.description = request.form.get("description")
            main_product.price = request.form.get("price")
            db.session.commit()
            flash("The product have been edited successfully", category="success")
            return redirect(url_for("upload.upload"))
        else:
            flash("The product does not exist", category="error")


@edit.route("/delete_product/<product_id>")
@login_required
def delete_product(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    if product:
        filename = product.filename
        path = os.path.join(app.config["UPLOAD_DIRECTORY"], filename)
        db.session.delete(product)
        db.session.commit()
        os.remove(path)
        flash("The product have been deleted successfully", category="success")
        return redirect(url_for("upload.upload"))
    else:
        flash("The product does not exist !!", category="error")
