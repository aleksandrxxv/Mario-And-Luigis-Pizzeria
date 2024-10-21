from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = "Secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.dpznsagmfkgblxagagdm:YR*QgPD9n.k#u9x@aws-0-eu-north-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def initialize_cart():
    if 'cart' not in session:
        session['cart'] = []

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    PizzaName = db.Column(db.String(100))
    PizzaPrice = db.Column(db.Float)
    PizzaToppings = db.Column(db.Text)
    PizzaImage = db.Column(db.Text)

    def get_toppings_list(self):
        return json.loads(self.PizzaToppings) if self.PizzaToppings else []

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    OrderTime = db.Column(db.String(100))
    OrderContents = db.Column(db.Text)
    OrderPlace = db.Column(db.String(100))
    OrderStatus = db.Column(db.String(100))


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    all_items = MenuItem.query.all()
    return render_template('menu.html', items = all_items)

@app.route('/addtocart', methods = ['POST'])
def addtocart():

    initialize_cart()

    pizza = MenuItem.query.get(request.form.get('id'))

    topping = request.form.get('topping').capitalize()
    pizza_size = request.form.get('pizza_size').capitalize()
    pizza_price = pizza.PizzaPrice
    pizza_name = pizza.PizzaName
    quantity = int(request.form.get('quantity'))

    item = {
        'pizza_name' : pizza_name,
        'pizza_size' : pizza_size,
        'pizza_price' : pizza_price,
        'topping' : topping,
        'quantity' : quantity
    }

    session['cart'].append(item)
    session.modified = True

    return redirect(url_for('view_cart'))


@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])

    return render_template('cart.html', cart = cart)

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None)
    return redirect(url_for('index'))

