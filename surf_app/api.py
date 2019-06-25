from flask import (
    Blueprint, redirect, url_for, render_template, g, session, request, flash,
    jsonify
    )
import json
from surf_app.models import User,Post, UserRelations
from surf_app import db

bp = Blueprint('api', __name__,url_prefix='/api')

@bp.route('/users/<int:id>',methods=('GET',))
def get_user(id):
    user = User.query.get_or_404(id)
    return json.dumps(user.to_dict())

@bp.route('/users',methods=('GET',))
def get_users():
    page = request.args.get('page',1, type=int)
    per_page = min(request.args.get('per_page',10, type=int), 20)
    data = User.to_paginated_dict(User.query, page, per_page,'api.get_users')
    return jsonify(data)

@bp.route('/users/<int:id>/followers',methods=('GET',))
def get_followers(id):
    page = request.args.get('page',1, type=int)
    per_page = min(request.args.get('per_page',10, type=int), 20)
    user = User.query.get_or_404(id)
    data = User.to_paginated_dict(user.followers, page, per_page,'api.get_followers',id=id)
    return jsonify(data)

@bp.route('/users/<int:id>/followed',methods=('GET',))
def get_followed(id):
    page = request.args.get('page',1,type=int)
    per_page = min(request.args.get('per_page',10,type=int), 20)
    user = User.query.get_or_404(id)
    data = User.to_paginated_dict(user.followed, page, per_page, 'api.get_followed',id=id)
    return jsonify(data)

@bp.route('/users',methods=('POST',))
def create_user():
    data = request.args or {}
    if 'username' not in data or 'password' not in data:
        return "Error username and password must be included"
    if User.query.filter_by(username=data['username']).first():
        return "Username: {} already exists, please use a different username".format(data['username'])

    user = User()
    user.from_dict(data, new_user=True)

    db.session.add(user)
    db.session.commit()

    response = jsonify(user.to_dict())
    response.status_code = 201

    return response

"""
Uncomment the update_user API once, authentication is implemented
"""
# @bp.route('/users/<int:id>',methods=('PUT',))
# def update_user(id):
#     data = request.args or {}
#     user = User.query.get_or_404(id)
#
#     if 'username' in data and data['username']!=user.username and \
#         User.query.filter_by(username=data['username']):
#         return "Please choose a different username"
#
#     user.from_dict(data, new_user=False)
#     db.session.commit()
#
#     return jsonify(user.to_dict())
