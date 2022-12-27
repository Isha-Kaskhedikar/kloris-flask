from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, EmailField, PasswordField, FileField
from wtforms.validators import DataRequired, Length

class TodoForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    description = TextAreaField('description',validators=[DataRequired()])
    completed = SelectField('Completed', choices = [("False", "False"), ("True", "True")], validators = [DataRequired()])
    submit = SubmitField("Add todo")

class registerform(FlaskForm):
    uname = StringField('Please enter your username', validators=[DataRequired()])
    email = EmailField('Please enter your Email', validators=[DataRequired()])
    passwd = PasswordField('password',validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")

class loginform(FlaskForm):
    uname = StringField('Username', validators=[DataRequired()])
    passwd = PasswordField('password',validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Login")

class plantform(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    Sciname = StringField('Scientific name')
    description = TextAreaField('description',validators=[DataRequired()])
    plantinginstruction = TextAreaField('Planting Instructions')
    caretips = TextAreaField('Planting Care Tips')
    img = StringField('Image link',validators=[DataRequired()])
    submit = SubmitField("Add Plant")
