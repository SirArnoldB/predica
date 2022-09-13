from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db
from .utils.apis import get_avg_housing_increase_or_decrease, get_job_inc_or_dec

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("index.html")

@views.route('/predica', methods=['GET', 'POST'])
def predica():
    if not session.get("name"):
        return redirect(url_for('views.login'))
    return render_template("predica.html")

@views.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == "POST":
        session["name"] = request.form['first_name']
        return redirect(url_for('views.predica'))
    return render_template("signup.html")

@views.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        if not session.get("name"):
            session["name"] = request.form['first_name']
        return redirect(url_for('views.predica'))
    return render_template("login.html")

@views.route('/logout')
def logout():
    session.pop("name", default=None)
    return redirect(url_for('views.index'))

@views.route('/simulate', methods=['GET','POST'])
def simulate():
    if request.method == "POST":
        zip_code = request.form['zip_code']
        num_years = int(request.form['number_of_years'])
        '''
        gender, race, and income are very important to consider
        however, due to insufficient info (and to avoid artificial bias), this model is not taking them into acccount
        there's generally a +ve correlation between income and occupation but factors like gender
        and race may also impact that - as more info is made available, this will be updated
        '''
        gender = request.form['gender']
        race = request.form['race']
        household_income = int(request.form['household_income'].replace(",",""))
        occupation = request.form['occupation']
        housing_percent = get_avg_housing_increase_or_decrease(zip_code, num_years)
        job_percent = get_job_inc_or_dec(occupation, num_years)  
        x,y = job_percent, housing_percent
        if y > 0 and x < 0:
            session['score'] = 1
        elif y > 0 and x > 0:
            session['score'] = 2
        elif y < 0 and x < 0:
            session['score'] = 3
        else:
            session['score'] = 4
        print(session['score'])
        flash("Score has been calculated!")
    return redirect(url_for('views.predica'))

