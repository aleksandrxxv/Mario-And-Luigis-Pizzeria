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
    order_placer = db.Column(db.String(100))
    order_time = db.Column(db.String(100))
    order_contents = db.Column(db.Text)
    order_place = db.Column(db.String(100))
    order_status = db.Column(db.String(100))


with app.app_context():
    db.create_all()

@app.route('/dev')
def dev():
    return render_template('dev.html')

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

@app.route('/checkout', methods = ['GET','POST'])
def checkout():
    cart = session.get('cart', [])
    name = request.form.get("name")
    order_place = request.form.get("place").capitalize()


    if cart:
        cart_json = json.dumps(cart)

        new_order = Orders(order_placer = name, order_time = datetime.datetime.now(), order_contents=cart_json, order_place=order_place, order_status="Received")

        db.session.add(new_order)
        db.session.commit()

        session.pop('cart', None)

        return "Order Placed"
    else:
        return "Your Cart is empty"

@app.route('/view_orders')
def view_orders():
    orders = Orders.query.all()

    orders_with_cart = []
    for order in orders:
        order_cart = json.loads(order.order_contents)
        orders_with_cart.append({
            'id': order.id,
            'order_time': order.order_time,
            'cart_items': order_cart,
            'order_place': order.order_place,
            'order_status': order.order_status,
            'order_placer': order.order_placer  
        })
    return render_template('orders.html', orders=orders_with_cart)

@app.route('/track_order/<order_placer>')
def track_order(order_placer):
    orders = Orders.query.filter_by(order_placer = order_placer).all()

    orders_with_cart = []
    for order in orders:
        order_cart = json.loads(order.order_contents)
        orders_with_cart.append({
            'id': order.id,
            'order_time': order.order_time,
            'cart_items': order_cart,
            'order_place': order.order_place,
            'order_status': order.order_status
        })
    return render_template('orders.html', orders=orders_with_cart)


