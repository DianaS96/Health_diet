from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
import os
from forms import Registration_From, Login_From
from models import User, db
import sqlite3

app = Flask(__name__)

#The database URI that should be used for the connection.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    conn = get_products_connected()
    prod = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return render_template('index.html', prod=prod)

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
#@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="localhost", port=8000)