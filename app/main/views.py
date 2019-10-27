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

@main.route('/post/<int:post_id>' ,methods=['GET', 'POST'])
def post(post_id):
    form = CommentForm()
    post = Post.query.filter_by(id=post_id).one()
    comments=Comment.get_comments(post_id)

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comment(comment=comment, post_id=post_id)

        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('main.post_comments', post_id=post.id))

    return render_template('post.html', post=post, form=form, comments=comments)    

@main.route('/post_comments/<int:post_id>' ,methods=['GET', 'POST'])
def post_comments(post_id):

    post = Post.query.filter_by(id=post_id).one()
    comments=Comment.get_comments(post_id)

    return render_template('post_comments.html', post=post, comments=comments, post_id=post.id)  

@main.route('/post/delete/<int:post_id>' ,methods=['GET', 'POST'])
@login_required
def delete_post(post_id):

    post = Post.query.filter_by(id=post_id).one()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('.index', post=post, post_id=post.id))  


@main.route('/comment/delete/<int:post_id>' ,methods=['GET', 'POST'])
@login_required
def delete_comment(post_id):

    post = Post.query.filter_by(id=post_id).first()
    comment = Comment.query.filter_by(post_id=post_id).first()

    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('.post_comments', comment=comment, post=post, post_id=post.id))         