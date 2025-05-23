from flask import Flask, render_template, redirect, url_for
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

# defining database file path
db_path = os.path.abspath("financer.db")


class Base(DeclarativeBase):
    pass


# initializing flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app, model_class=Base)


# class defination
class Mlimani(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expense: Mapped[int] = mapped_column(Integer, nullable=False)
    tcash: Mapped[int] = mapped_column(Integer, nullable=False)
    paybill: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)


class Kings(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expense: Mapped[int] = mapped_column(Integer, nullable=False)
    tcash: Mapped[int] = mapped_column(Integer, nullable=False)
    paybill: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)


class Administrator(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    expenditure: Mapped[int] = mapped_column(Integer, nullable=False)
    to_im: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        phone_no = form.phone_no.data
        password = form.password.data
        if phone_no == "0707070707" and password == "evans":
            return redirect(url_for("mlimani"))
        if phone_no == "0700000000" and password == "viola":
            return redirect(url_for("kings"))
        if phone_no == "0702988621" and password == "sam":
            return redirect(url_for("admin"))
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
        db.session.add(new_submission)
        db.session.commit()
        return redirect(url_for("home"))
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
        db.session.add(new_submission)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("kings.html", form=form)


@app.route("/admin", methods=["POST", "GET"])
def admin():
    form = Admin()
    """Chart for mlimani"""

    mdates = []
    mtotal_cash = []
    mpaybill = []
    mexpenditure = []
    mlimani = db.session.execute(db.select(Mlimani)).scalars().all()

    for record in mlimani:
        mdates.append(record.date)
        mexpenditure.append(record.expense)
        mtotal_cash.append(record.tcash)
        mpaybill.append(record.paybill)

    trace1 = go.Scatter(x=mdates, y=mexpenditure, name='Expenditure', mode='lines+markers')
    trace2 = go.Scatter(x=mdates, y=mpaybill, name='Paybill', mode='lines+markers')
    trace3 = go.Scatter(x=mdates, y=mtotal_cash, name='Total Cash', mode='lines+markers')

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
    ktotal_cash = []
    kpaybill = []
    kexpenditure = []
    kings = db.session.execute(db.select(Kings)).scalars().all()

    for record in kings:
        kdates.append(record.date)
        kexpenditure.append(record.expense)
        ktotal_cash.append(record.tcash)
        kpaybill.append(record.paybill)

    trace1 = go.Scatter(x=kdates, y=kexpenditure, name='Expenditure', mode='lines+markers')
    trace2 = go.Scatter(x=kdates, y=kpaybill, name='Paybill', mode='lines+markers')
    trace3 = go.Scatter(x=kdates, y=ktotal_cash, name='Total Cash', mode='lines+markers')

    data = [trace1, trace2, trace3]
    layout = go.Layout(
        title='Cashflow Overview - Kings',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Amount'),
    )

    fig = go.Figure(data=data, layout=layout)
    chart_div_kings = pyo.plot(fig, output_type='div', include_plotlyjs=False)

    if form.validate_on_submit():
        expenditure = form.expenditure.data
        to_im = form.to_im.data

        new_submission = Administrator(
            expenditure=expenditure,
            to_im=to_im
        )
        db.session.add(new_submission)
        db.session.commit()
        return redirect(url_for("home"))
    today = date.today()
    yesterday = today - timedelta(days=2)

    #todays records
    mlimani_today = db.session.execute(db.select(Mlimani).where(Mlimani.date == today)).scalars().all()
    for record in mlimani_today:
        mlimani_total_cash = record.tcash
        mlimani_paybill = record.paybill


    #yesterday's records
    mlimani_yesterday = db.session.execute(db.select(Mlimani).where(Mlimani.date == yesterday)).scalars().all()
    for record in mlimani_yesterday:
        mlimani_total_cash_yesterday = record.tcash

    mlimani_today_cash= mlimani_total_cash - mlimani_total_cash_yesterday

    """Kings cash today"""
    kings_today = db.session.execute(db.select(Kings).where(Kings.date == today)).scalars().all()
    for record in kings_today:
        kings_total_cash = record.tcash
        kings_paybill = record.paybill

    """Kings cash yesterday"""
    kings_yesterday = db.session.execute(db.select(Mlimani).where(Mlimani.date == yesterday)).scalars().all()
    for record in kings_yesterday:
        kings_total_cash_yesterday = record.tcash

    kings_today_cash = kings_total_cash - kings_total_cash_yesterday

    # admin_today = db.session.execute(db.select(Administrator).where(Administrator.date == today)).scalars().all()
    # for record in admin_today:
    #     admin_expenditure= record.expenditure

    active_balance = (mlimani_today_cash + mlimani_paybill + kings_today_cash + kings_paybill)
    print(active_balance)

    return render_template("admin.html", form=form, chart_div=chart_div,
                       chart_div_kings=chart_div_kings, active_balance=active_balance)

if __name__ == "__main__":
    app.run(debug=True)
