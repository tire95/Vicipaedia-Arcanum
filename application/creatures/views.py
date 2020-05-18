from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required
from application.creatures.models import Creature
from application.creatures.forms import CreatureForm, ModifyForm


@app.route("/creatures", methods=["GET"])
@login_required
def creatures_index():
    return render_template("creatures/list.html", creatures=db.session.query(Creature).all())


@app.route("/creatures/new/")
@login_required
def creatures_form():
    return render_template("creatures/new.html", form = CreatureForm())


@app.route("/creatures/<creature_id>/remove/", methods=["POST"])
@login_required
def remove_creature(creature_id):

    db.session.query(Creature).filter_by(id=creature_id).delete()
    db.session().commit()
  
    return redirect(url_for("creatures_index"))


@app.route("/creatures/", methods=["POST"])
@login_required
def creatures_create():
    form = CreatureForm(request.form)

    creature = db.session.query(Creature).filter_by(name=form.name.data).first()
    if creature:
        return render_template("creatures/new.html", form = form,
                               error = "A creature with such a name already exists")

    if not form.validate():
        return render_template("creatures/new.html", form = form)

    creature_to_add = Creature(form.name.data, form.type.data, form.size.data, form.notes.data)

    db.session().add(creature_to_add)
    db.session().commit()

    return redirect(url_for("creatures_index"))


@app.route("/creatures/<creature_id>/", methods=["GET"])
@login_required
def open_creature(creature_id):
    return render_template("creatures/creature.html", creature=db.session.query(Creature).get(creature_id))


@app.route("/creatures/<creature_id>/modify", methods=["GET", "POST"])
@login_required
def modify_creature(creature_id):
    creature = db.session.query(Creature).get(creature_id)
    form = ModifyForm(request.form)

    if request.method == "GET":
        form.type.data = creature.type
        form.size.data = creature.size
        form.notes.data = creature.notes
        return render_template("creatures/modify.html", creature_id = creature_id, form = form, creature = creature)

    if not form.validate():
        return render_template("creatures/modify.html", creature_id = creature_id, form = form, creature = creature)

    creature.type = form.type.data
    creature.size = form.size.data
    creature.notes = form.notes.data

    db.session.commit()

    return redirect(url_for("open_creature", creature_id=creature_id))
