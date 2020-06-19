from flask import render_template
from application import app, db
from application.campaigns.models import Campaign
from application.creatures.models import Creature
from application.npcs.models import Npc
from sqlalchemy import func

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/art")
def art():
    return render_template("art.html")

@app.route("/stats")
def stats():
    nmbr_of_campaigns = db.session.query(func.count(Campaign.id)).scalar()
    nmbr_of_creatures = db.session.query(func.count(Creature.id)).scalar()
    nmbr_of_npcs = db.session.query(func.count(Npc.id)).scalar()
    average_of_creatures_for_campaigns = Campaign.average_of_creatures_for_campaigns()
    average_of_npcs_for_campaigns = Campaign.average_of_npcs_for_campaigns()
    return render_template("stats.html", nmbr_of_campaigns=nmbr_of_campaigns, nmbr_of_creatures=nmbr_of_creatures, nmbr_of_npcs=nmbr_of_npcs, average_of_creatures_for_campaigns=average_of_creatures_for_campaigns, average_of_npcs_for_campaigns=average_of_npcs_for_campaigns)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(405)
def page_wrong_method(e):
    return render_template('405.html'), 405