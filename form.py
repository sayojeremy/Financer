from flask_wtf import FlaskForm
from wtforms import StringField ,IntegerField, DateField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length,NumberRange

# form for personal money in
class InForm(FlaskForm):
    source = StringField("Source of funds", validators=[DataRequired()])
    amount = StringField("Amount", validators=[DataRequired()])
    date = DateField("Date Received", validators=[DataRequired()])
    submit = SubmitField("Okay!")

# form for personal money out
class OutForm(FlaskForm):
    expense = StringField("Expense", validators=[DataRequired()])
    amount = StringField("Amount", validators=[DataRequired()])
    date = DateField("Date Spent", validators=[DataRequired()])
    notes= StringField("Further Notes", validators=[DataRequired()])
    submit = SubmitField("Okay!")