from application import db, bcrypt

# Association table between accounts and campaigns
association_table = db.Table('association',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaign.id'))
)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    name = db.Column(db.String(50), nullable=False)
    game_system = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(144), nullable=True)

    creatures = db.relationship("Creature", backref="campaign", lazy=True)
    accounts = db.relationship("Account", secondary=association_table)

    def __init__(self, name, game_system, password):
        self.name = name
        self.game_system = game_system
        if password:
            self.password = bcrypt.generate_password_hash(password).decode("utf8")

# Function for checking whether a certain user is already registered to a campaign 
def check_account(campaign_id, user):
    return db.session.query(Campaign).filter(Campaign.id==campaign_id).filter(Campaign.accounts.contains(user)).first()