from flask import (
    Blueprint, redirect, url_for, render_template, g, session, request, flash,
    jsonify
    )
import json
from surf_app.models import User,Post, UserRelations

bp = Blueprint('api', __name__,url_prefix='/api')

@bp.route('/users/<int:id>',methods=('GET',))
def get_user(id):
    user = User.query.filter_by(id=id).first()
    return json.dumps(user.to_dict())

@bp.route('/users',methods=('GET',))
def get_users():
    pass

@bp.route('/users/<int:id>/followers',methods=('GET',))
def get_followers(id):
    pass

@bp.route('/users/<int:id>/followed',methods=('GET',))
def get_followed(id):
    pass

@bp.route('/users',methods=('POST',))
def create_user():
    pass

@bp.route('/users/<int:id>',methods=('PUT',))
def update_user(id):
    pass
