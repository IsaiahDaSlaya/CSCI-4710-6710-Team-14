from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    if "cart" not in session:
        flash("There is nothing in your cart.")
        return render_template("cart.html", display_cart = {}, total = 0)
    else:
        items = session["cart"]
        dict_of_melons = {}

        total_price = 0
        for item in items:
            melon = model.get_melon_by_id(item)
            total_price += melon.price
            if melon.id in dict_of_melons:
                dict_of_melons[melon.id]["qty"] += 1
            else:
                dict_of_melons[melon.id] = {"qty":1, "name": melon.common_name, "price":melon.price}
        
        return render_template("cart.html", display_cart = dict_of_melons, total = total_price)  
    

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    if "cart" not in session:
        session["cart"] = []

    session["cart"].append(id)

    flash("Successfully added to cart!")
    return redirect("/cart")


@app.route("/checkout")
def checkout():
    flash("Success! An Order Confirmation will be sent to your email shortly.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
