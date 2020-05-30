from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
  
class LoginForm(FlaskForm):
    name = StringField("Name", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Username"})
    password = PasswordField("Password", [validators.InputRequired(), validators.Length(min=8)], render_kw={"placeholder": "Password"})
  
    class Meta:
        csrf = False

class RegisterForm(FlaskForm):
    register_name = StringField("Name", [validators.InputRequired(), validators.Length(min=2, max=144)], render_kw={"placeholder": "Username"})
    register_password = PasswordField("Password", [validators.InputRequired(), validators.Length(min=8)], render_kw={"placeholder": "Password"})
  
    class Meta:
        csrf = False
