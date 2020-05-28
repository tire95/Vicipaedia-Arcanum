from application import db, bcrypt
from application.models import NameBase
from sqlalchemy.sql import text


class Account(NameBase):
  
    password = db.Column(db.String(144), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = bcrypt.generate_password_hash(password).decode("utf8")
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    @staticmethod
    def number_of_joined_campaigns(account_id):
        stmt = text("SELECT COUNT(campaign.id) FROM Campaign INNER JOIN association ON campaign.id = association.campaign_id " 
        "INNER JOIN Account ON association.account_id = account.id WHERE account.id = :account_id").params(account_id=account_id)
        return db.engine.execute(stmt).scalar()
