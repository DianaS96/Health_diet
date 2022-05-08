import flask.json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, flash, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
import os
import forms
from forms import Registration_From, Login_From, Select_product, Select_date
from models import User, db, Users_info
import sqlite3
from datetime import datetime, date
import pandas as pd
from sqlalchemy import func
import plotly as py
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from utils import get_totals_PFC

app = Flask(__name__)


# The database URI that should be used for the connection.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_BINDS'] = {
    'users_info':   'sqlite:///users_info.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

# creating LoginManager class - this lets my application and Flask-Login work together
login_manager = LoginManager()
login_manager.init_app(app)

db.init_app(app)


# create the USER table and database
@app.before_first_request
def create_table():
    db.create_all(app=app)
    db.create_all(bind='users_info')


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


@app.route('/diary_add', methods=['POST', 'GET'])
#@login_required
def diary_add():
    form = Select_product()
    conn = get_products_connected()
    prod = conn.execute('SELECT DISTINCT(type) FROM products').fetchall()
    prod_type = conn.execute('SELECT type, product FROM products').fetchall()
    form.type.choices += [item['type'] for item in prod]
    form.product.choices = [product['product'] for product in filter(lambda c: c[0] == "Баранина_и_дичь", prod_type)]

    if form.submit.data:
       # prod = conn.execute('SELECT product FROM products WHERE type={goal}'.format(goal=f'"{types}"')).fetchall()
        cals = conn.execute('SELECT * FROM products WHERE type={goal} and product={goal1}'.format(goal=f'"{form.type.data}"', goal1=f'"{form.product.data}"')).fetchone()

        user_info = Users_info(meal=form.meal.data,
                               user=current_user.username,
                               date=form.date.data,
                               date_str=form.date.data.strftime('%d-%m-%Y'),
                               type=form.type.data,
                               product=form.product.data,
                               amount=form.amount.data,
                               calories=round(float(cals['calories']) * float(form.amount.data) / 100, 2),
                               proteins=round(float(cals['proteins']) * float(form.amount.data) / 100, 2),
                               fats=round(float(cals['fats']) * float(form.amount.data) / 100, 2),
                               carbohydrates=round(float(cals['carbohydrates']) * float(form.amount.data) / 100, 2))
        db.session.add(user_info)
        db.session.commit()
        return redirect(url_for('diary_add', form=form))
    return render_template('diary_add.html', form=form)


@app.route('/diary_show', methods=['POST', 'GET'])
#@login_required
def diary_show():

    form_date = Select_date()

    data_choices = Users_info.query.filter_by(user=current_user.username).all()
    form_date.date.choices += [item.date_str for item in data_choices]

    if form_date.submit.data:
        d = Users_info.query.filter_by(user=current_user.username, date_str=form_date.date.data).order_by(Users_info.date.desc()).all()
    #    conn.close()

        sum_amount, sum_cal, sum_prot, sum_fats, sum_co2 = get_totals_PFC(form_date)

        product_amount_per_day = db.session.query(Users_info.product, db.func.sum(Users_info.amount)).\
            filter_by(user=current_user.username, date_str=form_date.date.data).\
            group_by(Users_info.product).all()

        type_amount_per_day = db.session.query(Users_info.type, db.func.sum(Users_info.amount)).\
            filter_by(user=current_user.username, date_str=form_date.date.data).\
            group_by(Users_info.type).all()

        df_product = pd.DataFrame(data=product_amount_per_day, columns=['Product', 'Amount'])
        df_type = pd.DataFrame(data=type_amount_per_day, columns=['Type', 'Amount'])
        print(df_type)

        fig = make_subplots(rows=1, cols=1, specs=[[{'type':'domain'}]])

        fig.add_trace(go.Pie(labels=df_type['Type'],
                             values=df_type['Amount'],
                             name='Breakdown by type of product', legendgroup=1), 1, 1)
        #fig.add_trace(go.Pie(labels=df_product['Product'],
         #                    values=df_product['Amount'],
          #                   name='Breakdown by product', legendgroup=2), 1, 2)

        fig.update_traces(hole=.4, hoverinfo="label+percent+name")

        fig.update_layout(
            title_text="Breakdown of meals by type and product, %",
            # Add annotations in the center of the donut pies.
            annotations=[dict(text='Type', x=0.18, y=0.5, font_size=20, showarrow=False)])

        graphJSON = json.dumps(fig, cls=py.utils.PlotlyJSONEncoder)

        sum_PFC = sum_prot + sum_cal + sum_co2

        labels = ['Proteins', 'Fats', 'Carbohydrates']
        values = [(round(float(sum_prot / sum_PFC), 2)),
                  (round(float(sum_fats / sum_PFC), 2)),
                  (round(float(sum_co2 / sum_PFC), 2))]

        fig1 = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        graphJSON1 = json.dumps(fig1, cls=py.utils.PlotlyJSONEncoder)

        return render_template('diary_show.html', date=form_date, user=d,
                               sum_cal=round(sum_cal, 2),
                               sum_amount=round(sum_amount, 2),
                               sum_prot=round(sum_prot, 2),
                               sum_fats=round(sum_fats, 2),
                               sum_co2=round(sum_co2, 2),
                               plot_pie_chart_products=graphJSON,
                               plot_pie_chart_pfc=graphJSON1)
    return render_template('diary_show.html', date=form_date)


@app.route('/product/<types>', methods=['POST', 'GET'])
def product(types):
    conn = get_products_connected()
    prod = conn.execute('SELECT product FROM products WHERE type={goal}'.format(goal=f'"{types}"')).fetchall()

    prod_arr = []

    for pr in prod:
        prObj = {}
        prObj['product'] = pr['product']
        prod_arr.append(prObj)

    return flask.json.jsonify({'prod_arr':prod_arr})


if __name__ == "__main__":
    app.run(host="localhost", port=8000)