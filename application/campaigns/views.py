from flask import render_template, request, redirect, url_for

from application import app, db, bcrypt
from application.campaigns.models import Campaign, check_account
from application.campaigns.forms import CampaignForm, RegisterForm
from flask_login import login_required, current_user
from application.auth.models import Account


@app.route("/campaigns/new", methods = ["GET", "POST"])
@login_required
def campaigns_create():
    if request.method == "GET":
        return render_template("campaigns/new.html", form = CampaignForm())

    form = CampaignForm(request.form)

    if db.session.query(Campaign).filter(Campaign.name.ilike(form.name.data)).first():
        return render_template("campaigns/new.html", form = form,
                                error = "A campaign with such a name already exists")

    if not form.validate():
        return render_template("campaigns/new.html", form = form)

    campaign_to_add = Campaign(form.name.data, form.game_system.data, form.password.data)
    campaign_to_add.accounts.append(current_user)

    db.session().add(campaign_to_add)
    db.session().commit()

    return redirect(url_for("campaigns_index"))


@app.route("/campaigns", methods=["GET"])
@login_required
def campaigns_index():
    return render_template("campaigns/list.html", joined_campaigns=db.session.query(Campaign).filter(Campaign.accounts.contains(current_user)),
        not_joined_campaigns=db.session.query(Campaign).filter(~Campaign.accounts.contains(current_user)), 
        number_of_joined_campaigns=Account.number_of_joined_campaigns(current_user.id))


@app.route("/campaigns/register/<campaign_id>", methods=["GET", "POST"])
@login_required
def campaigns_register(campaign_id):

    campaign = db.session.query(Campaign).filter_by(id=campaign_id).first()
    form = RegisterForm(request.form)

    # If the campaign has no password or the password is correct, register the account
    if not campaign.password or (form.validate() and bcrypt.check_password_hash(campaign.password, form.password.data)):
        campaign.accounts.append(current_user)
        db.session.commit()
        return redirect(url_for("campaigns_view", campaign_id = campaign_id))

    if request.method == "GET":
        return render_template("campaigns/register.html", form = RegisterForm(), campaign_id=campaign_id)

    return render_template("campaigns/register.html", form = form, campaign_id = campaign_id, error = "Wrong password")


@app.route("/campaigns/view/<campaign_id>/", methods=["GET"])
@login_required
def campaigns_view(campaign_id):
    if check_account(campaign_id, current_user):
        return render_template("campaigns/view.html", number_of_creatures=Campaign.number_of_creatures(campaign_id), number_of_npcs=Campaign.number_of_npcs(campaign_id), 
        campaign_id = campaign_id)
    else:
        return redirect(url_for("campaigns_register", campaign_id=campaign_id))



    