from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import *
from ..models import *
from flask_login import login_required, current_user
from .. import db,photos
import markdown2
from ..email import mail_message

@main.route('/')
def index():
    posts = Post.query.order_by(Post.date_posted.desc()).all()

    return render_template('index.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html')    