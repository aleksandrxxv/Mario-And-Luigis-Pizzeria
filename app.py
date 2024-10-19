from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = "Secret key"

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.dpznsagmfkgblxagagdm:YR*QgPD9n.k#u9x@aws-0-eu-north-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    PizzaName = db.Column(db.String(100))
    PizzaPrice = db.Column(db.Float)
    PizzaToppings = db.Column(db.Text)
    PizzaImage = db.Column(db.Text)

    def get_toppings_list(self):
        print(self.PizzaToppings)
        return json.loads(self.PizzaToppings) if self.PizzaToppings else []


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    all_items = MenuItem.query.all()
    return render_template('menu.html', items = all_items)