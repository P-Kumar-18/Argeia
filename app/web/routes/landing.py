from flask import render_template
from . import main


@main.route("/")
def landing():
    return render_template('landing_page.html')