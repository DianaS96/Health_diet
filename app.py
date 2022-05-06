import flask.json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
import os

import forms
from forms import Registration_From, Login_From, Select_product
from models import User, db
import sqlite3

app = Flask(__name__)

#The database URI that should be used for the connection.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

# creating LoginManager class - this lets my application and Flask-Login work together
login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)

#create the USER table and database
@app.before_first_request
def create_table():
    db.create_all(app=app)

# Info about SECRET_KEY usage: https://flask.palletsprojects.com/en/2.1.x/config/
# Flask-Login uses sessions for authentication,
# secret key is used to encrypting the cookies in session,
# the user could look at the contents of cookie but not modify it,
# unless they know the secret key used for signing.
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

# A user loader tells Flask-Login how to get a specific user object
# from the ID that is stored in the session cookie
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def get_products_connected():
    conn = sqlite3.connect('products.db')
    conn.row_factory = sqlite3.Row
    return conn

# Returning homepage template
@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')

# Register
@app.route('/register', methods=['POST', 'GET'])
def register():
    form = Registration_From()
    if form.validate_on_submit():
        if (db.session.query(User).filter_by(email=form.email.data).count() < 1 and
                db.session.query(User).filter_by(username=form.username.data).count() < 1):
            user = User(username=form.username.data, email=form.email.data)
        else:
            flash("User with such Name or email already exists")
            return render_template('registration.html', form=form)
        user.set_pswd(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('registration.html', form=form)

# Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login_From()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_pswd(form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash("Invalid email or password!")
    return render_template('login.html', form=form)

# Logout
@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/products_table', methods=['POST', 'GET'])
@login_required
def products_table():
    conn = get_products_connected()
    prod = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('products_table.html', prod=prod)

@app.route('/diary', methods=['POST', 'GET'])
#@login_required
def diary():
    form = Select_product()
    conn = get_products_connected()
    prod = conn.execute('SELECT DISTINCT(type) FROM products').fetchall()
    prod_type = conn.execute('SELECT type, product FROM products').fetchall()
    form.type.choices += [item['type'] for item in prod]
    form.product.choices = [product['product'] for product in filter(lambda c: c[0] == "Бобовые", prod_type)]
    conn.close()
    if request.method == "POST":
        pr = filter(lambda c: c[0] == "Бобовые", prod_type)
        return '<h1>Type: {}; Product: {} <\h1>'.format(form.type.data, next(pr)['product'])
    return render_template('diary.html', form=form)

@app.route('/product/<types>', methods=['POST', 'GET'])
def product(types):
    conn = get_products_connected()
    prod = conn.execute('SELECT product FROM products WHERE type={goal}'.format(goal=f'"{types}"')).fetchall()

    prod_arr = []

    for pr in prod:
        prObj = {}
        prObj['product'] = pr['product']
        prod_arr.append(prObj)

    return flask.json.jsonify({'types':prod_arr})

if __name__ == "__main__":
    app.run(host="localhost", port=8000)