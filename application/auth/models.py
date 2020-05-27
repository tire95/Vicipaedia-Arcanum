from application import db, bcrypt
from application.models import NameBase


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
