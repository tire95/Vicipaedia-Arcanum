from application import db, bcrypt
from application.models import NameBase
from sqlalchemy.sql import text


# Association table between accounts and campaigns
association_table = db.Table('association',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
    db.Column('campaign_id', db.Integer, db.ForeignKey('campaign.id'))
)

class Campaign(NameBase):
    game_system = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=True)

    creatures = db.relationship("Creature", backref="campaign", lazy=True)
    accounts = db.relationship("Account", secondary=association_table)

    def __init__(self, name, game_system, password):
        self.name = name
        self.game_system = game_system
        if password:
            self.password = bcrypt.generate_password_hash(password).decode("utf8")

    @staticmethod
    def number_of_creatures(campaign_id):
        stmt = text("SELECT COUNT(creature.id) FROM Creature WHERE creature.campaign_id = :campaign_id").params(campaign_id=campaign_id)
        return db.engine.execute(stmt).scalar()

    @staticmethod
    def number_of_npcs(campaign_id):
        stmt = text("SELECT COUNT(NPC.id) FROM NPC WHERE NPC.campaign_id = :campaign_id").params(campaign_id=campaign_id)
        return db.engine.execute(stmt).scalar()


# Function for checking whether a certain user is already registered to a campaign 
def check_account(campaign_id, user):
    return db.session.query(Campaign).filter(Campaign.id==campaign_id).filter(Campaign.accounts.contains(user)).first()