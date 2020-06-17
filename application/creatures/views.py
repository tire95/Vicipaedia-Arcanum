from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.creatures.models import Creature
from application.creatures.forms import CreatureForm
from application.campaigns.models import Campaign



@app.route("/campaigns/<campaign_id>/creatures", methods=["GET"])
@login_required
def creatures_index(campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user):
        return render_template("creatures/list.html", creatures=db.session.query(Creature).filter_by(campaign_id=campaign_id).all(),
         campaign_id=campaign_id)
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))


@app.route("/campaigns/<campaign_id>/creatures/new/")
@login_required
def creatures_form(campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user):
        return render_template("creatures/new.html", form = CreatureForm(), campaign_id=campaign_id)
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))


@app.route("/campaigns/<campaign_id>/creatures/<creature_id>/remove/", methods=["POST"])
@login_required
def remove_creature(creature_id, campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user) and Campaign.is_campaign_admin(campaign_id, current_user):
        db.session.query(Creature).filter_by(id=creature_id).delete()
        db.session().commit()
        return redirect(url_for("creatures_index", campaign_id=campaign_id))
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))



@app.route("/campaigns/<campaign_id>/creatures/", methods=["POST"])
@login_required
def creatures_create(campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user):

        form = CreatureForm(request.form)

        if db.session.query(Creature).filter(Creature.creature_name.ilike(form.creature_name.data)).filter(Creature.campaign_id==campaign_id).first():
            return render_template("creatures/new.html", form = form,
                                error = "A creature with such a name already exists", campaign_id=campaign_id)

        if not form.validate():
            return render_template("creatures/new.html", form = form, campaign_id=campaign_id)

        creature_to_add = Creature(form.creature_name.data, form.type.data, form.size.data, form.description.data, campaign_id)

        db.session().add(creature_to_add)
        db.session().commit()

        return redirect(url_for("creatures_index", campaign_id=campaign_id))

    return redirect(url_for("campaigns_register", campaign_id=campaign_id))



@app.route("/campaigns/<campaign_id>/creatures/<creature_id>/", methods=["GET"])
@login_required
def open_creature(creature_id, campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user):
        return render_template("creatures/creature.html", creature=db.session.query(Creature).get(creature_id), campaign_id=campaign_id, user_is_admin=Campaign.is_campaign_admin(campaign_id, current_user))
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))


@app.route("/campaigns/<campaign_id>/creatures/<creature_id>/modify", methods=["GET", "POST"])
@login_required
def modify_creature(creature_id, campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user):

        creature = db.session.query(Creature).get(creature_id)
        form = CreatureForm(request.form)

        if request.method == "GET":
            form.creature_name.data = creature.creature_name
            form.type.data = creature.type
            form.size.data = creature.size
            form.description.data = creature.description
            return render_template("creatures/modify.html", creature_id = creature_id, form = form, creature = creature, campaign_id=campaign_id)

        if not form.validate():
            return render_template("creatures/modify.html", creature_id = creature_id, form = form, creature = creature, campaign_id=campaign_id)

        # If trying to change the name, check whether a creature with the new name already exists
        if not creature.creature_name == form.creature_name.data:
            if db.session.query(Creature).filter(Creature.creature_name.ilike(form.creature_name.data)).filter(Creature.campaign_id==campaign_id).first():
                return render_template("creatures/modify.html", creature_id = creature_id, form = form, creature = creature, campaign_id=campaign_id, error = "A creature with such a name already exists")
            else:
                creature.creature_name = form.creature_name.data

        creature.type = form.type.data
        creature.size = form.size.data
        creature.description = form.description.data

        db.session.commit()

        return redirect(url_for("open_creature", creature_id=creature_id, campaign_id=campaign_id))

    return redirect(url_for("campaigns_register", campaign_id=campaign_id))

