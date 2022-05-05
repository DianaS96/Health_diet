from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from forms import Registration_From, Login_From

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)

#init SQLAlchemy
db = SQLAlchemy()
db.init_app(app)
@app.before_first_request
def create_table():
    db.create_all(app=app)
SECRET_KEY = os.urandom(32)

app.config['SECRET_KEY'] = SECRET_KEY

# creating LoginManager class - this lets my application and Flask-Login work together

class User(UserMixin, db.Model):
    # create field 'id'
    id = db.Column(db.Integer, primary_key=True)
    # create field 'username' (string with the max size of 50 chars)
    username = db.Column(db.String(50), index=True, unique=True)
    # create field 'email' (string with the max size of 50 chars)
    email = db.Column(db.String(50), index=True, unique=True)

    pswd_hash = db.Column(db.String(50))
    date_joined = db.Column(db.DateTime(), default=datetime.utcnow, index=True)

    def set_pswd(self, password):
        self.pswd_hash = generate_password_hash(password)

    def check_pswd(self, password):
        return (check_password_hash(self.pswd_hash, password))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')


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

@app.route('/logout', methods=['POST', 'GET'])
#@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="localhost", port=8000)