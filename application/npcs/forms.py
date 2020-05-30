from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators
 
class NpcForm(FlaskForm):
    name = StringField("NPC's name", [validators.InputRequired(), validators.Length(min=2, max=144)])
    race = StringField("NPC's race", [validators.InputRequired(), validators.Length(min=2, max=144)])
    location = StringField("NPC's location", [validators.InputRequired(), validators.Length(min=2, max=144)])
    occupation = StringField("NPC's occupation", [validators.InputRequired(), validators.Length(min=2, max=144)])
    description = TextAreaField("Description about the NPC", [validators.Length(max=1000)])

    class Meta:
        csrf = False


class ModifyForm(FlaskForm):
    race = StringField("NPC's race", [validators.InputRequired(), validators.Length(min=2, max=144)])
    location = StringField("NPC's location", [validators.InputRequired(), validators.Length(min=2, max=144)])
    occupation = StringField("NPC's occupation", [validators.InputRequired(), validators.Length(min=2, max=144)])
    description = TextAreaField("Description about the NPC", [validators.Length(max=1000)])

    class Meta:
        csrf = False    
