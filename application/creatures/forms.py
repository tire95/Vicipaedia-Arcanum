from flask_wtf import FlaskForm
from wtforms import StringField, validators

class CreatureForm(FlaskForm):
    name = StringField("Creature name", [validators.Length(min=2, max=20)])
    type = StringField("Creature type", [validators.Length(min=2, max=10)])
    size = StringField("Creature size", [validators.Length(min=2, max=10)])
    notes = StringField("Notes about the creature", [validators.Length(max=144)])
 
    class Meta:
        csrf = False