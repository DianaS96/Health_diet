from models import User, db, Users_info
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required

def get_totals_PFC(form_date):
    sum_amount = Users_info.query.filter_by(user=current_user.username, date_str=form_date.date.data). \
        with_entities(func.sum(Users_info.amount).label('total')).first().total

    sum_cal = Users_info.query.filter_by(user=current_user.username, date_str=form_date.date.data). \
        with_entities(func.sum(Users_info.calories).label('total')).first().total

    sum_prot = Users_info.query.filter_by(user=current_user.username, date_str=form_date.date.data). \
        with_entities(func.sum(Users_info.proteins).label('total')).first().total

    sum_fats = Users_info.query.filter_by(user=current_user.username, date_str=form_date.date.data). \
        with_entities(func.sum(Users_info.fats).label('total')).first().total

    sum_co2 = Users_info.query.filter_by(user=current_user.username, date_str=form_date.date.data). \
        with_entities(func.sum(Users_info.carbohydrates).label('total')).first().total

    return (sum_amount, sum_cal, sum_prot, sum_fats, sum_co2)