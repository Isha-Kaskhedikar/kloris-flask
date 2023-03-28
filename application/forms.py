from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, EmailField, PasswordField, FileField, IntegerField,FloatField
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

class queform(FlaskForm):
    question = StringField('Question')
    bodyy = StringField('Body')
    image = StringField('Image link')
    submit = SubmitField("Add Question")

class replyform(FlaskForm):
    question = StringField('Question') #-------joh title (main question hai) 
    answer = StringField('Add Comment') #---------joh voh khud uss title ke thread mein comment karna chahta hai
    submit = SubmitField("Submit")

class quessform(FlaskForm):
    light = IntegerField('Light_Intensity')
    height = IntegerField('Height')
    spread = IntegerField('Spread')
    usee= StringField('Use')
    lat = FloatField('Latitude')
    long = FloatField('Longitude')
    submit = SubmitField("Submit")