from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import Required,Email,EqualTo
from ..models import *
from wtforms import ValidationError
from wtforms import StringField,PasswordField,BooleanField,SubmitField