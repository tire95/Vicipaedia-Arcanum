from flask import render_template
from application import app

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/art")
def art():
    return render_template("art.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(405)
def page_wrong_method(e):
    return render_template('405.html'), 405