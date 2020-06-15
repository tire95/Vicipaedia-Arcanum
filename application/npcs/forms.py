from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators
 
class NpcForm(FlaskForm):
    name = StringField("NPC's name", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "NPC's name"})
    race = StringField("NPC's race", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "NPC's race"})
    location = StringField("NPC's location", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "NPC's location"})
    occupation = StringField("NPC's occupation", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "NPC's occupation"})
    description = TextAreaField("Description about the NPC", [validators.Length(max=1000)], render_kw={"placeholder": "Description about the NPC"})

