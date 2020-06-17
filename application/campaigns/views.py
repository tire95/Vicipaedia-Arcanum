from flask import render_template, request, redirect, url_for

from application import app, db, bcrypt
from application.campaigns.models import Campaign
from application.campaigns.forms import CampaignForm, RegisterForm, DeleteForm, PasswordForm
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

    campaign_to_add = Campaign(form.name.data, form.game_system.data, form.password.data, current_user.id)
    campaign_to_add.accounts.append(current_user)

    db.session().add(campaign_to_add)
    db.session().commit()

    return redirect(url_for("campaigns_list"))


@app.route("/campaigns", methods=["GET"])
@login_required
def campaigns_list():
    joined_campaigns=db.session.query(Campaign).filter(Campaign.accounts.contains(current_user))
    number_of_joined_campaigns=Account.number_of_joined_campaigns(current_user.id)
    return render_template("campaigns/list.html", joined_campaigns=joined_campaigns,
        number_of_joined_campaigns=number_of_joined_campaigns)


@app.route("/campaigns/<campaign_id>/register/", methods=["POST"])
@login_required
def campaigns_register(campaign_id):

    campaign = db.session.query(Campaign).filter_by(id=campaign_id).first()
    form = RegisterForm(request.form)

    # If the campaign has no password or the password is correct, register the account
    if not campaign.password or (form.validate() and bcrypt.check_password_hash(campaign.password, form.password.data)):
        campaign.accounts.append(current_user)
        db.session.commit()
        return redirect(url_for("campaigns_view", campaign_id = campaign_id))

    return render_template("campaigns/register.html", form = form, campaign_id = campaign_id)


@app.route("/campaigns/<campaign_id>/view/", methods=["GET"])
@login_required
def campaigns_view(campaign_id):
    campaign = db.session.query(Campaign).filter_by(id=campaign_id).first()
    return render_template("campaigns/view.html", number_of_creatures=Campaign.number_of_creatures(campaign_id), number_of_npcs=Campaign.number_of_npcs(campaign_id), 
        campaign_id = campaign_id, campaign_name = campaign.name, user_is_admin=Campaign.is_campaign_admin(campaign_id, current_user))


    return redirect(url_for("campaigns_register", campaign_id=campaign_id))


@app.route("/campaigns/<campaign_id>/admin", methods=["GET"])
@login_required
def campaigns_admin_view(campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user) and Campaign.is_campaign_admin(campaign_id, current_user):
        campaign = db.session.query(Campaign).filter_by(id=campaign_id).first()
        accounts=Campaign.joined_accounts(campaign_id, current_user.id)
        number_of_joined_accounts=Campaign.number_of_joined_accounts(campaign_id, current_user.id)
        return render_template("campaigns/admin.html", campaign_id=campaign_id, accounts=accounts, number_of_joined_accounts=number_of_joined_accounts, campaign_name=campaign.name)
    else:
        return redirect(url_for("campaigns_view", campaign_id = campaign_id))


@app.route("/campaigns/<campaign_id>/admin/<account_id>/remove/", methods=["POST"])
@login_required
def campaigns_remove_account(account_id, campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user) and Campaign.is_campaign_admin(campaign_id, current_user):
        Campaign.remove_account(account_id, campaign_id)
        return redirect(url_for("campaigns_admin_view", campaign_id=campaign_id))
    else:
        return redirect(url_for("campaigns_view", campaign_id = campaign_id))


@app.route("/campaigns/<campaign_id>/admin/remove_campaign", methods=["GET", "POST"])
@login_required
def campaigns_remove(campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user) and Campaign.is_campaign_admin(campaign_id, current_user):
        campaign = db.session.query(Campaign).filter_by(id=campaign_id).first()
        if request.method == "GET":
            return render_template("campaigns/remove.html", campaign_id = campaign_id, form = DeleteForm(), campaign_name = campaign.name)

        form = DeleteForm(request.form)

        if form.validate():
            campaign = db.session.query(Campaign).filter(Campaign.id==campaign_id).first()
            if (not campaign.password or bcrypt.check_password_hash(campaign.password, form.password.data)) and campaign.name == form.name.data:
                db.session.delete(campaign)
                db.session.commit()
                return redirect(url_for("campaigns_list"))

        return render_template("campaigns/remove.html", campaign_id = campaign_id, form = form, campaign_name = campaign.name, error = "Wrong name and/or password")

    else:
        return redirect(url_for("campaigns_view", campaign_id = campaign_id))


@app.route("/campaigns/<campaign_id>/admin/change_password", methods=["GET", "POST"])
@login_required
def campaigns_change_password(campaign_id):
    if Campaign.is_registered_to_campaign(campaign_id, current_user) and Campaign.is_campaign_admin(campaign_id, current_user):
        if request.method == "GET":
            return render_template("campaigns/change_password.html", campaign_id = campaign_id, form = PasswordForm())

        form = PasswordForm(request.form)

        if form.validate():
            campaign = db.session.query(Campaign).filter(Campaign.id==campaign_id).first()
            if not campaign.password or bcrypt.check_password_hash(campaign.password, form.old_password.data):
                campaign.password = bcrypt.generate_password_hash(form.new_password.data).decode("utf8")
                db.session.commit()
                return redirect(url_for("campaigns_admin_view", campaign_id = campaign_id))
        return render_template("campaigns/change_password.html", campaign_id = campaign_id, form = form, error = "Wrong password")
    else:
        return redirect(url_for("campaigns_view", campaign_id = campaign_id))


@app.route("/campaigns/not_joined", methods=["GET"])
@login_required
def campaigns_list_not_joined():
    not_joined_campaigns=db.session.query(Campaign).filter(~Campaign.accounts.contains(current_user))
    return render_template("campaigns/list_not_joined.html", not_joined_campaigns=not_joined_campaigns)

