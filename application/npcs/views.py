from application import app, db
from flask import redirect, render_template, request, url_for
from flask_login import login_required, current_user
from application.npcs.models import Npc
from application.npcs.forms import NpcForm, ModifyForm
from application.campaigns.models import Campaign, check_account



@app.route("/campaigns/<campaign_id>/npcs", methods=["GET"])
@login_required
def npcs_index(campaign_id):
    if check_account(campaign_id, current_user):
        return render_template("npcs/list.html", npcs=db.session.query(Npc).filter_by(campaign_id=campaign_id).all(),
         campaign_id=campaign_id)
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))


@app.route("/campaigns/<campaign_id>/npcs/new/")
@login_required
def npcs_form(campaign_id):
    if check_account(campaign_id, current_user):
        return render_template("npcs/new.html", form = NpcForm(), campaign_id=campaign_id)
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))


@app.route("/campaigns/<campaign_id>/npcs/<npc_id>/remove/", methods=["POST"])
@login_required
def remove_npc(npc_id, campaign_id):
    if check_account(campaign_id, current_user):
        db.session.query(Npc).filter_by(id=npc_id).delete()
        db.session().commit()
        return redirect(url_for("npcs_index", campaign_id=campaign_id))
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))



@app.route("/campaigns/<campaign_id>/npcs/new/", methods=["POST"])
@login_required
def npcs_create(campaign_id):
    if check_account(campaign_id, current_user):
        
        form = NpcForm(request.form)

        if db.session.query(Npc).filter(Npc.name.ilike(form.name.data)).filter(Npc.campaign_id==campaign_id).first():
            return render_template("npcs/new.html", form = form,
                                error = "An NPC with such a name already exists", campaign_id=campaign_id)

        if not form.validate():
            return render_template("npcs/new.html", form = form, campaign_id=campaign_id)

        npc_to_add = Npc(form.name.data, form.race.data, form.location.data, form.occupation.data, form.description.data, campaign_id)

        db.session().add(npc_to_add)
        db.session().commit()

        return redirect(url_for("npcs_index", campaign_id=campaign_id))

    return redirect(url_for("campaigns_register", campaign_id=campaign_id))



@app.route("/campaigns/<campaign_id>/npcs/<npc_id>/", methods=["GET"])
@login_required
def open_npc(npc_id, campaign_id):
    if check_account(campaign_id, current_user):
        return render_template("npcs/npc.html", npc=db.session.query(Npc).get(npc_id), campaign_id=campaign_id)
    return redirect(url_for("campaigns_register", campaign_id=campaign_id))


@app.route("/campaigns/<campaign_id>/npcs/<npc_id>/modify", methods=["GET", "POST"])
@login_required
def modify_npc(npc_id, campaign_id):
    if check_account(campaign_id, current_user):

        npc = db.session.query(Npc).get(npc_id)
        form = ModifyForm(request.form)

        if request.method == "GET":
            form.race.data = npc.race
            form.location.data = npc.location
            form.occupation.data = npc.occupation
            form.description.data = npc.description
            return render_template("npcs/modify.html", npc_id = npc_id, form = form, npc = npc, campaign_id=campaign_id)

        if not form.validate():
            return render_template("npcs/modify.html", npc_id = npc_id, form = form, npc = npc, campaign_id=campaign_id)

        npc.race = form.race.data
        npc.location = form.location.data
        npc.occupation = form.occupation.data
        npc.description = form.description.data

        db.session.commit()

        return redirect(url_for("open_npc", npc_id=npc_id, campaign_id=campaign_id))

    return redirect(url_for("campaigns_register", campaign_id=campaign_id))

