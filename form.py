from flask_wtf import FlaskForm
from wtforms import StringField ,IntegerField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired

# form for personal money in
class InForm(FlaskForm):
    expense = IntegerField("Expenditure", validators=[DataRequired()])
    tcash = IntegerField("Total cash", validators=[DataRequired()])
    paybill = IntegerField("Paybill", validators=[DataRequired()])
    submit = SubmitField("Okay!")

class Admin(FlaskForm):
    expenditure = IntegerField("Expenditure")
    to_im = IntegerField("Transfer to I&M")
    submit = SubmitField("Okay!")

# Create a form to login existing users
class LoginForm(FlaskForm):
    phone_no = StringField("Phone Number", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")
