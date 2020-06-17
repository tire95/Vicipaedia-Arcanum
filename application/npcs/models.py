from application import db
from application.models import BaseModel


class Npc(BaseModel):
    
    npc_name = db.Column(db.String(144), nullable=False)
    race = db.Column(db.String(144), nullable=False)
    location = db.Column(db.String(144), nullable=False)
    occupation = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, npc_name, race, location, occupation, description, campaign_id):
        self.npc_name = npc_name
        self.race = race
        self.location = location
        self.occupation = occupation
        self.description = description
        self.campaign_id = campaign_id
