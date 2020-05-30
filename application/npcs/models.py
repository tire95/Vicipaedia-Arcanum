from application import db
from application.models import NameBase


class NPC(NameBase):
    race = db.Column(db.String(144), nullable=False)
    location = db.Column(db.String(144), nullable=False)
    occupation = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

    def __init__(self, name, race, location, occupation, description, campaign_id):
        self.name = name
        self.race = race
        self.location = location
        self.occupation = occupation
        self.description = description
        self.campaign_id = campaign_id
