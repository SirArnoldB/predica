from flask import Blueprint, render_template, request, redirect, url_for
from . import db
from .utils.apis import get_avg_housing_increase_or_decrease

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template("index.html")

@views.route('/predica')
def predica():
    return render_template("index.html")

@views.route('/simulate', methods=['GET','POST'])
def simulate():
    if request.method == "POST":
        zip_code = request.form['zip_code']
        num_years = request.form['number_of_years']
        result = get_avg_housing_increase_or_decrease(zip_code, num_years)
        return render_template("simulated_analysis.html", result=result)
    return redirect(url_for('views.index'))
