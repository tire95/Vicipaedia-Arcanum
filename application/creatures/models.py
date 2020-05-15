from application import db


class Creature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    name = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    notes = db.Column(db.String(144), nullable=True)

    def __init__(self, name, type, size, notes):
        self.name = name
        self.type = type
        self.size = size
        self.notes = notes
