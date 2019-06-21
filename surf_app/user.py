from flask import (
    Blueprint, url_for, redirect, session, render_template, flash, g, request
)

from surf_app.auth import login_required
import requests
from surf_app.models import User, Post, UserRelations
from surf_app import db

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/<username>')
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    user_posts = user.get_posts()
    # Making call to our API to access user information
    # user_api_url = "http://localhost:5000/api/users/{}".format(user.id)
    # user_api_response = requests.get(user_api_url)
    # try:
    #     user_api_response.raise_for_status()
    # except Exception as exc:
    #     print("There was a problem with SURF API:",(exc))
    # user_details = user_api_response.json()

    user_details = user.to_dict()
    return render_template('user/user_profile.html', user=user_details, posts=user_posts,
        is_following=user.is_following(username))

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
        flash('You are already following {}.format(username)')
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
