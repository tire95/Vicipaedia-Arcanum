from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.npcs.models import Npc
from application.npcs.forms import NpcForm
from application.campaigns.models import Campaign



@app.route("/campaigns/<campaign_id>/npcs", methods=["GET"])
@login_required
def npcs_index(campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user):
        return render_template("npcs/list.html", npcs=db.session.query(Npc).filter_by(campaign_id=campaign_id).all(),
         campaign_id=campaign_id)
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))


@app.route("/campaigns/<campaign_id>/npcs/new/")
@login_required
def npcs_form(campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user):
        return render_template("npcs/new.html", form = NpcForm(), campaign_id=campaign_id)
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))


@app.route("/campaigns/<campaign_id>/npcs/<npc_id>/remove/", methods=["POST"])
@login_required
def remove_npc(npc_id, campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user) and Campaign.is_campaign_admin(campaign_id, current_user):
        db.session.query(Npc).filter_by(id=npc_id).delete()
        db.session().commit()
        return redirect(url_for("npcs_index", campaign_id=campaign_id))
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))



@app.route("/campaigns/<campaign_id>/npcs/new/", methods=["POST"])
@login_required
def npcs_create(campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user):
        
        form = NpcForm(request.form)

        if db.session.query(Npc).filter(Npc.npc_name.ilike(form.npc_name.data)).filter(Npc.campaign_id==campaign_id).first():
            return render_template("npcs/new.html", form = form,
                                error = "An NPC with such a name already exists", campaign_id=campaign_id)

        if not form.validate():
            return render_template("npcs/new.html", form = form, campaign_id=campaign_id)

        npc_to_add = Npc(form.npc_name.data, form.race.data, form.location.data, form.occupation.data, form.description.data, campaign_id)

        db.session().add(npc_to_add)
        db.session().commit()

        return redirect(url_for("npcs_index", campaign_id=campaign_id))

    return redirect(url_for("campaigns_register", campaign_id=campaign_id))



@app.route("/campaigns/<campaign_id>/npcs/<npc_id>/", methods=["GET"])
@login_required
def open_npc(npc_id, campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user):
        return render_template("npcs/npc.html", npc=db.session.query(Npc).get(npc_id), campaign_id=campaign_id, user_is_admin=Campaign.is_campaign_admin(campaign_id, current_user))
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))


@app.route("/campaigns/<campaign_id>/npcs/<npc_id>/modify", methods=["GET", "POST"])
@login_required
def modify_npc(npc_id, campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user):

        npc = db.session.query(Npc).get(npc_id)
        form = NpcForm(request.form)

        if request.method == "GET":
            form.npc_name.data = npc.npc_name
            form.race.data = npc.race
            form.location.data = npc.location
            form.occupation.data = npc.occupation
            form.description.data = npc.description
            return render_template("npcs/modify.html", npc_id = npc_id, form = form, npc = npc, campaign_id=campaign_id)

        if not form.validate():
            return render_template("npcs/modify.html", npc_id = npc_id, form = form, npc = npc, campaign_id=campaign_id)
        
        # If trying to change the name, check whether an npc with the new name already exists
        if not npc.npc_name == form.npc_name.data:
            if db.session.query(Npc).filter(Npc.npc_name.ilike(form.npc_name.data)).filter(Npc.campaign_id==campaign_id).first():
                return render_template("npcs/modify.html", npc_id = npc_id, form = form, npc = npc, campaign_id=campaign_id, error = "An NPC with such a name already exists")
            else:
                npc.npc_name = form.npc_name.data

        npc.race = form.race.data
        npc.location = form.location.data
        npc.occupation = form.occupation.data
        npc.description = form.description.data

        db.session.commit()

        return redirect(url_for("open_npc", npc_id=npc_id, campaign_id=campaign_id))

    return redirect(url_for("campaigns_register", campaign_id=campaign_id))

