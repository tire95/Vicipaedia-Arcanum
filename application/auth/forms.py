from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(), validators.Length(min=2, max=144)])
    password = PasswordField("Password", [validators.InputRequired(), validators.InputRequired(message="Password required")])
  
    class Meta:
        csrf = False
