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

    creatures = db.relationship("Creature", backref="campaign", lazy=True, cascade="all,delete")
    npcs = db.relationship("Npc", backref="campaign", lazy=True, cascade="all,delete")
    accounts = db.relationship("Account", secondary=association_table)
    admin_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, name, game_system, password, admin_id):
        self.name = name
        self.game_system = game_system
        if password:
            self.password = bcrypt.generate_password_hash(password).decode("utf8")
        self.admin_id = admin_id

    @staticmethod
    def number_of_creatures(campaign_id):
        stmt = text("SELECT COUNT(creature.id) FROM Creature WHERE creature.campaign_id = :campaign_id").params(campaign_id=campaign_id)
        return db.engine.execute(stmt).scalar()

    @staticmethod
    def number_of_npcs(campaign_id):
        stmt = text("SELECT COUNT(Npc.id) FROM Npc WHERE Npc.campaign_id = :campaign_id").params(campaign_id=campaign_id)
        return db.engine.execute(stmt).scalar()

    # Function for getting all accounts in a campaign; does not return the admin's account so admin can't remove themselves from the campaign
    @staticmethod
    def joined_accounts(campaign_id, account_id):
        stmt = text("SELECT id, name FROM Account INNER JOIN association ON Account.id = association.account_id AND association.campaign_id = :campaign_id AND NOT Account.id = :account_id").params(campaign_id=campaign_id, account_id=account_id)
        results = db.engine.execute(stmt)

        response = []
        for row in results:
            response.append({"id":row[0], "name":row[1]})

        return response

    @staticmethod
    def remove_account(account_id, campaign_id):
        stmt = text("DELETE FROM association WHERE association.account_id = :account_id AND association.campaign_id = :campaign_id").params(account_id=account_id, campaign_id=campaign_id)
        db.engine.execute(stmt)

    # Function for checking whether a certain user is already registered to a campaign 
    @staticmethod
    def is_registered_to_campaign(campaign_id, user):
        return db.session.query(Campaign).filter(Campaign.id==campaign_id).filter(Campaign.accounts.contains(user)).first()

    # Function for checking whether a certain user is admin of a campaign
    @staticmethod
    def is_campaign_admin(campaign_id, user):
        campaign = db.session.query(Campaign).filter(Campaign.id==campaign_id).first()
        return campaign.admin_id == user.id