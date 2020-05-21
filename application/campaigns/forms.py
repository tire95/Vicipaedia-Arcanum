from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class CampaignForm(FlaskForm):
    name = StringField("Campaign's name", [validators.Length(min=2, max=50)])
    game_system = StringField("Game system (e.g. D&D 5e, Pathfinder)", [validators.Length(min=2, max=50)])
    password = PasswordField("Campaign's password")
  
    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    password = PasswordField("Campaign's password", [validators.Length(min=1)])
  
    class Meta:
        csrf = False        
