from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators

class CreatureForm(FlaskForm):
    creature_name = StringField("Creature name", [validators.DataRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Creature's name"})
    type = StringField("Creature type", [validators.DataRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Creature's type"})
    size = StringField("Creature size", [validators.DataRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Creature's size"})
    description = TextAreaField("Description about the creature", [validators.Length(max=1000)], render_kw={"placeholder": "Description about the creature"})
 
