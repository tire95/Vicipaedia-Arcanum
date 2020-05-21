from application import db


class Creature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    name = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    notes = db.Column(db.String(1000), nullable=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)

    def __init__(self, name, type, size, notes, campaign_id):
        self.name = name
        self.type = type
        self.size = size
        self.notes = notes
        self.campaign_id = campaign_id
