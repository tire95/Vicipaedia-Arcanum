from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
 
class CampaignForm(FlaskForm):
    campaign_name = StringField("Campaign's name", [validators.DataRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Campaign's name"})
    game_system = StringField("Game system (e.g. D&D 5e, Pathfinder)", [validators.DataRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Game system (e.g. D&D 5e, Pathfinder)"})
    password = PasswordField("Campaign's password", render_kw={"placeholder": "Campaign's password"})


class RegisterForm(FlaskForm):
    password = PasswordField("Campaign's password", [validators.DataRequired()], render_kw={"placeholder": "Campaign's password"})


class DeleteForm(FlaskForm):
    campaign_name = StringField("Campaign's name", [validators.DataRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Campaign's name"})
    password = PasswordField("Campaign's password", render_kw={"placeholder": "Campaign's password"})
  


class PasswordForm(FlaskForm):
    old_password = PasswordField("Old password", render_kw={"placeholder": "Old password"})
    new_password = PasswordField("New password", [validators.DataRequired()], render_kw={"placeholder": "New password"})
        
