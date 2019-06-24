from flask import (
    Blueprint, url_for, redirect, session, render_template, flash, g, request
)

from surf_app.auth import login_required
import requests
from surf_app.models import User, Post, UserRelations
from surf_app import db
from werkzeug.exceptions import abort

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<username>')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        abort(404,"User with username {} doesn't exist".format(username))

    user_posts = user.get_posts()
    user_details = user.to_dict()
    return render_template('user/user_profile.html', user=user_details, posts=user_posts,
        is_following=g.user.is_following(username))

@bp.route('/edit_profile', methods=('GET','POST'))
@login_required
def edit_profile():

    if request.method=='POST':
        input_username = request.form['username']
        about_me = request.form['about_me']

        if input_username != g.user.username:
            if User.query.filter_by(username=input_username).first():
                abort(403, "Username {} already in use".format(input_username))

        g.user.username = input_username
        g.user.about_me = about_me
        db.session.commit()
        return redirect(url_for('user.user_profile',username=input_username))

    return render_template('user/edit_profile.html', user=g.user)



@bp.route('/follow/<username>')
@login_required
def follow(username):
    current_user = g.user
    follow_user = User.query.filter_by(username=username).first()

    if follow_user is None:
        flash('User {} does not exist'.format(username))
        return redirect(url_for('blog.index'))
    elif follow_user.id==session['user_id']:
        flash('You can\'t Follow yourself')
        return redirect(url_for('blog.index'))
    elif current_user.is_following(username):
        flash("You are already following {}".format(username))
        return redirect(url_for('user.user_profile',username=username))

    relation = UserRelations(follower_id=g.user.id, followed_id=follow_user.id)
    db.session.add(relation)
    db.session.commit()
    flash("You have succesfully followed {}".format(username))

    return redirect(url_for('user.user_profile',username=username))

@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    error = None
    current_user = g.user

    unfollow_user = User.query.filter_by(username=username).first()

    if unfollow_user is None:
        flash('User {} does not exist'.format(username))
        return redirect(url_for('blog.index'))

    UserRelations.query.filter_by(follower_id=current_user.id,followed_id=unfollow_user.id).delete()
    db.session.commit()
    flash("You have succesfully unfollowed {}".format(username))
    return redirect(url_for('user.user_profile',username=username))
