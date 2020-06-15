from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators

class CreatureForm(FlaskForm):
    name = StringField("Creature name", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Creature's name"})
    type = StringField("Creature type", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Creature's type"})
    size = StringField("Creature size", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Creature's size"})
    description = TextAreaField("Description about the creature", [validators.Length(max=1000)], render_kw={"placeholder": "Description about the creature"})
 
