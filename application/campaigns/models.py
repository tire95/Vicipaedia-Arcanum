from application import db, bcrypt


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    name = db.Column(db.String(50), nullable=False)
    game_system = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(144), nullable=True)

    creatures = db.relationship("Creature", backref="campaign", lazy=True)

    def __init__(self, name, game_system, password):
        self.name = name
        self.game_system = game_system
        if password:
            self.password = bcrypt.generate_password_hash(password)