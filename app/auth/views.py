from flask import render_template,redirect,url_for, flash,request
from . import auth
from ..models import *
from flask_login import login_user,logout_user,login_required
from .forms import LoginForm,RegistrationForm
from ..email import mail_message
from .. import db
