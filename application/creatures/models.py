from application import db
from application.models import BaseModel


class Creature(BaseModel):
    
    creature_name = db.Column(db.String(144), nullable=False)
    type = db.Column(db.String(144), nullable=False)
    size = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, creature_name, type, size, description, campaign_id):
        self.creature_name = creature_name
        self.type = type
        self.size = size
        self.description = description
        self.campaign_id = campaign_id
