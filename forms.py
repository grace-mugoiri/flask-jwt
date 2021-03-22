from wtforms import Form, BooleanField, StringField, PasswordField, \
    validators, TextAreaField, IntegerField

from wtforms.validators import DataRequired


class LoginForm(Form):
    email = StringField("Email", validators=[validators.Length(min=7, max=50), validators.DataRequired(message="Fill this form")])
	  password = PasswordField("Password", validators=[validators.DataRequired(message="Please add a password")])


class RegisterForm(Form):
	name = StringField("Name", validators=[validators.Length(min=3, max=30), validators.DataRequired(message="Add name")])
	username = StringField("Username", validators=[validators.Length(min=3, max=30), validators.DataRequired(message="Add username")])
	email = StringField("Email", validators.DataRequired(message="Enter a valid email")])
	password = PasswordField("Password", validators=[validators.DataRequired(message="Please fill field"), validators.EqualTo(fieldname="confirm", message="Your passwords do not match")])
	confirm_passwordd = PasswordField("Confirm Password", validators=[validators.DataRequired(message="Please fill field"), validators.EqualTo(fieldname="confirm", message="Your passwords do not match")])
