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

@main.route('/add',methods=['GET', 'POST'])
@login_required
def add():

    form=AddPost()

    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        content = form.content.data

        post = Post(title=title, subtitle=subtitle, content=content, user_id=current_user.id, date_posted=datetime.now())


        db.session.add(post)
        db.session.commit()
        return redirect(url_for('.post',form=form, post_id=post.id))
    return render_template('add_blog.html', form=form) 

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user) 
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))   

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required

def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)                  