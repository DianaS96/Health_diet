from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange
from wtforms.widgets import html_params

class Registration_From(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    pswd_confirm = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class Login_From(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('Remember', validators=[DataRequired()])
    submit = SubmitField('Log in')

class Select_product(FlaskForm):
    type = SelectField('type', choices=[])
    product = SelectField('product', choices=[])
    amount = IntegerField('amount', validators=[DataRequired(), NumberRange(min=1, max=1000)])