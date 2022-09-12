from flask import Blueprint, render_template
from . import db
from .utils.apis import get_avg_housing_increase_or_decrease

views = Blueprint('views', __name__)

@views.route('/')
def index():
    zipCode = "07083"
    res = get_avg_housing_increase_or_decrease(zipCode, 10)
    return render_template("index.html", res=res)