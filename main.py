from flask import Flask, render_template, redirect, url_for, flash
from form import InForm, Admin, LoginForm
import requests
from datetime import date, timedelta
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, Float, Date, func, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column
import plotly.graph_objs as go
import plotly.offline as pyo
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv
load_dotenv()

# defining database file path
db_path = os.path.abspath("financer.db")


class Base(DeclarativeBase):
    pass


# initializing flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("secret_key")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app, model_class=Base)



# class defination
class Mlimani(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expense: Mapped[int] = mapped_column(Integer, nullable=False)
    tcash: Mapped[int] = mapped_column(Integer, nullable=False)
    paybill: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False, unique= True)


class Kings(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expense: Mapped[int] = mapped_column(Integer, nullable=False)
    tcash: Mapped[int] = mapped_column(Integer, nullable=False)
    paybill: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False, unique =True)


class Administrator(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expenditure: Mapped[int] = mapped_column(Integer, nullable=False)
    to_im: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False, unique = True)

class Today(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mlimani_today_cash: Mapped[int] = mapped_column(Integer, nullable=False)
    kings_today_cash: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False, unique= True)

class Balance(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    active_balance: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False, unique= True)

with app.app_context():
    db.create_all()


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        phone_no = form.phone_no.data
        password = form.password.data
        mlimani_phone_no = os.getenv("mlimani_phone_no")
        mlimani_password = os.getenv("mlimani_password")
        kings_phone_no = os.getenv("kings_phone_no")
        kings_password = os.getenv("kings_password")
        admin_phone_no = os.getenv("admin_phone_no")
        admin_password = os.getenv("admin_password")
        if phone_no == mlimani_phone_no and password == mlimani_password:
            return redirect(url_for("mlimani"))
        elif phone_no == kings_phone_no and password == kings_password:
            return redirect(url_for("kings"))
        elif phone_no == admin_phone_no and password == admin_password:
            return redirect(url_for("admin_form"))
        else:
            flash("Invalid login details!", "danger")
    return render_template("login.html", form=form)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/mlimani", methods=["POST", "GET"])
def mlimani():
    form = InForm()
    if form.validate_on_submit():
        expense = form.expense.data
        tcash = form.tcash.data
        paybill = form.paybill.data

        new_submission = Mlimani(
            expense=expense,
            tcash=tcash,
            paybill=paybill
        )
        try:
            db.session.add(new_submission)
            db.session.commit()
            flash("Record submitted successfully!", "success")
        except IntegrityError:
            db.session.rollback()  # Always rollback on failure before continuing
            flash("A record for today already exists.", "warning")
        return redirect(url_for("mlimani"))
    return render_template("mlimani.html", form=form)


@app.route("/kings", methods=["POST", "GET"])
def kings():
    form = InForm()
    if form.validate_on_submit():
        expense = form.expense.data
        tcash = form.tcash.data
        paybill = form.paybill.data

        new_submission = Kings(
            expense=expense,
            tcash=tcash,
            paybill=paybill
        )
        try:
            db.session.add(new_submission)
            db.session.commit()
            flash("Record submitted successfully!", "success")
        except IntegrityError:
            db.session.rollback()  # Always rollback on failure before continuing
            flash("A record for today already exists.", "warning")
        return redirect(url_for("kings"))
    return render_template("kings.html", form=form)

@app.route("/admin_form", methods= ["POST", "GET"])
def admin_form():
    form = Admin()
    if form.validate_on_submit():
        expenditure = form.expenditure.data
        to_im = form.to_im.data

        new_submission = Administrator(
            expenditure=expenditure,
            to_im=to_im
        )
        try:
            db.session.add(new_submission)
            db.session.commit()
            flash("Record submitted successfully!", "success")
        except IntegrityError:
            db.session.rollback()  # Always rollback on failure before continuing
            flash("A record for today already exists.", "warning")
        return redirect(url_for("admin"))
    return render_template("admin_form.html", form= form)

@app.route("/admin", methods=["POST", "GET"])
def admin():

    """Chart for mlimani"""
    """Data entered is total cash cumulative from sunday. Cash per day is the difference between yesterday's and 
    today's cash reset on every sunday"""

    #step 1: Get today and yesterday as time deltas
    today = date.today()

    yesterday = today - timedelta(days=1)


    #step 2: Get mlimani records for today and yaesterday. mlimani_today cash is the cash collected per day
    """Mlimani today records"""
    mlimani_today = db.session.execute(db.select(Mlimani).where(Mlimani.date == today)).scalars().all()
    for record in mlimani_today:
        mlimani_total_cash = record.tcash
        mlimani_paybill = record.paybill

    """Mlimani yesterday records"""
    mlimani_yesterday = db.session.execute(db.select(Mlimani).where(Mlimani.date == yesterday)).scalars().all()
    for record in mlimani_yesterday:
        mlimani_total_cash_yesterday = record.tcash

    """Money is always moved out of the account on monday. So if it monday, it is not cummulative balance but the data entered
    on that day"""
    is_monday = today.weekday() == 0
    if is_monday:
        mlimani_today_cash = mlimani_total_cash  # No subtraction, assume Sunday was reset to 0
    else:
        mlimani_today_cash = mlimani_total_cash - mlimani_total_cash_yesterday

    #step 3- Get kings records for today and yesterday. Kings_today_cash is the cash collected for the day
    """Kings cash today"""
    kings_today = db.session.execute(db.select(Kings).where(Kings.date == today)).scalars().all()
    for record in kings_today:
        kings_total_cash = record.tcash
        kings_paybill = record.paybill

    """Kings cash yesterday"""
    kings_yesterday = db.session.execute(db.select(Mlimani).where(Kings.date == yesterday)).scalars().all()
    for record in kings_yesterday:
        kings_total_cash_yesterday = record.tcash

    if is_monday:
        kings_today_cash = kings_total_cash
    else:
        kings_today_cash = kings_total_cash - kings_total_cash_yesterday

    # step 4: commiting the calculated values into a database
    existing = db.session.execute(db.select(Today).where(Today.date == today)).scalars().first()
    if not existing:
        new_today= Today(
            mlimani_today_cash = mlimani_today_cash,
            kings_today_cash = kings_today_cash
        )
        db.session.add(new_today)
        db.session.commit()

    admin_today = db.session.execute(db.select(Administrator).where(Administrator.date == today)).scalars().all()
    for record in admin_today:
        admin_expenditure = record.expenditure


    """calculation of active balance"""
    # Example: fetching last known balance
    previous_balance = db.session.execute(
        db.select(Balance).order_by(Balance.date.desc())
    ).scalar()

    if not previous_balance:
        previous_balance_amount = 0
    else:
        previous_balance_amount = previous_balance.active_balance

    # Calculate new balance
    today_sales = (mlimani_today_cash + mlimani_paybill + kings_today_cash + kings_paybill)
    active_balance = (previous_balance_amount + today_sales) - admin_expenditure
    new_balance= Balance(
        active_balance= active_balance
    )
    db.session.add(new_balance)
    db.session.commit()

    cash_today = db.session.execute(db.select(Today)).scalars().all()
    today_cash = []
    ktoday_cash = []
    for record in cash_today:
        today_cash.append(record.mlimani_today_cash)
        ktoday_cash.append(record.kings_today_cash)

    mdates = []
    mpaybill = []
    mexpenditure = []


    mlimani = db.session.execute(db.select(Mlimani)).scalars().all()

    for record in mlimani:
        mdates.append(record.date)
        mexpenditure.append(record.expense)
        mpaybill.append(record.paybill)

    trace1 = go.Scatter(x=mdates, y=mexpenditure, name='Expenditure', mode='lines+markers')
    trace2 = go.Scatter(x=mdates, y=mpaybill, name='Paybill', mode='lines+markers')
    trace3 = go.Scatter(x=mdates, y=today_cash, name='Total Cash', mode='lines+markers')


    data = [trace1, trace2, trace3]
    layout = go.Layout(
        title='Cashflow Overview - Mlimani',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Amount'),
    )

    fig = go.Figure(data=data, layout=layout)
    chart_div = pyo.plot(fig, output_type='div', include_plotlyjs=False)

    """Chart for kings"""
    kdates = []
    kpaybill = []
    kexpenditure = []
    kings = db.session.execute(db.select(Kings)).scalars().all()

    for record in kings:
        kdates.append(record.date)
        kexpenditure.append(record.expense)
        kpaybill.append(record.paybill)

    trace1 = go.Scatter(x=kdates, y=kexpenditure, name='Expenditure', mode='lines+markers')
    trace2 = go.Scatter(x=kdates, y=kpaybill, name='Paybill', mode='lines+markers')
    trace3 = go.Scatter(x=kdates, y=ktoday_cash, name='Total Cash', mode='lines+markers')

    data = [trace1, trace2, trace3]
    layout = go.Layout(
        title='Cashflow Overview - Kings',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Amount'),
    )

    fig = go.Figure(data=data, layout=layout)
    chart_div_kings = pyo.plot(fig, output_type='div', include_plotlyjs=False)


    return render_template("admin.html", chart_div=chart_div,
                       chart_div_kings=chart_div_kings, active_balance=active_balance)

if __name__ == "__main__":
    app.run(debug=True)
