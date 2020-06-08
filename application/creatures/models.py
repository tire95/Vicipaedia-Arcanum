from application import db
from application.models import NameBase


class Creature(NameBase):
    type = db.Column(db.String(144), nullable=False)
    size = db.Column(db.String(144), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)

    def __init__(self, name, type, size, description, campaign_id):
        self.name = name
        self.type = type
        self.size = size
        self.description = description
        self.campaign_id = campaign_id
