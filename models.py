from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

#init SQLAlchemy
db = SQLAlchemy()

# UserMixin will provide is_authenticated, is_active, is_anonymous and get_id()
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

class Users_info(db.Model):
    __bind_key__ = 'users_info'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    meal = db.Column(db.String(50))
    date = db.Column(db.DateTime)
    type = db.Column(db.String(500))
    product = db.Column(db.String(500))
    amount = db.Column(db.Integer)
