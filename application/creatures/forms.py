from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators

class CreatureForm(FlaskForm):
    name = StringField("Creature name", [validators.InputRequired(), validators.Length(min=2, max=20)])
    type = StringField("Creature type", [validators.InputRequired(), validators.Length(min=2, max=10)])
    size = StringField("Creature size", [validators.InputRequired(), validators.Length(min=2, max=10)])
    notes = TextAreaField("Notes about the creature", [validators.Length(max=1000)])
 
    class Meta:
        csrf = False

class ModifyForm(FlaskForm):
    type = StringField("Creature type", [validators.InputRequired(), validators.Length(min=2, max=10)])
    size = StringField("Creature size", [validators.InputRequired(), validators.Length(min=2, max=10)])
    notes = TextAreaField("Notes about the creature", [validators.Length(max=1000)])
 
    class Meta:
        csrf = False