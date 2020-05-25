from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    username = StringField("Username", [validators.InputRequired(), validators.Length(min=2, max=20)])
    password = PasswordField("Password", [validators.InputRequired(), validators.InputRequired(message="Password required")])
  
    class Meta:
        csrf = False
