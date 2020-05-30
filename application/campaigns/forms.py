from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
 
class CampaignForm(FlaskForm):
    name = StringField("Campaign's name", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Campaign's name"})
    game_system = StringField("Game system (e.g. D&D 5e, Pathfinder)", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Game system (e.g. D&D 5e, Pathfinder)"})
    password = PasswordField("Campaign's password", render_kw={"placeholder": "Campaign's password"})
  
    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    password = PasswordField("Campaign's password", [validators.InputRequired()], render_kw={"placeholder": "Campaign's password"})
  
    class Meta:
        csrf = False        
