from flask import Flask, render_template
from form import InForm, OutForm

app= Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/personal")
def personal():
    return render_template("personal.html")

@app.route("/company")
def company():
    return render_template("company.html")

@app.route("/personal_input", methods= ["POST", "GET"])
def personal_input():
    form= InForm()
    if form.validate_on_submit():
        source= form.source.data
        amount= form.amount.data
        date= form.date.data
        print(date)
        return "Sucess"
    return render_template("personal_input.html", form= form)

@app.route("/company_input", methods= ["POST", "GET"])
def company_input():
    form = InForm()
    if form.validate_on_submit():
        source = form.source.data
        amount = form.amount.data
        date = form.date.data
        print(date)
        return "Sucess"
    return render_template("company_input.html", form= form)

@app.route("/personal_output", methods = ["POST", "GET"])
def personal_output():
    form = OutForm()
    if form.validate_on_submit():
        expense= form.expense.data
        amount= form.amount.data
        date= form.date.data
        notes= form.notes.data
        print(notes)
        return "success"
    return render_template("personal_output.html", form= form)

@app.route("/company_output", methods = ["POST", "GET"])
def company_output():
    form = OutForm()
    if form.validate_on_submit():
        expense= form.expense.data
        amount= form.amount.data
        date= form.date.data
        notes= form.notes.data
        print(notes)
        return "success"
    return render_template("company_output.html", form= form)

if __name__ == "__main__":
    app.run(debug= True)


