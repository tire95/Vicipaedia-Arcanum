from application import app, db
from flask import redirect, render_template, request, url_for
from application.creatures.models import Creature


@app.route("/creatures", methods=["GET"])
def creatures_index():
    return render_template("creatures/list.html", creatures=Creature.query.all())


@app.route("/creatures/new/")
def creatures_form():
    return render_template("creatures/new.html")


@app.route("/creatures/", methods=["POST"])
def creatures_create():
    creature = Creature(request.form.get("name"), request.form.get(
        "type"), request.form.get("size"), request.form.get("notes"))

    db.session().add(creature)
    db.session().commit()

    return redirect(url_for("creatures_index"))
