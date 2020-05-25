from application import db, bcrypt


class Account(db.Model):
  
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(144), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
  
    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
