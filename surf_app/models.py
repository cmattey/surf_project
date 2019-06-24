from surf_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask import url_for


class PaginatedAPI():
    """
    Inherit this class to create Paginated APIs
    """
    @staticmethod
    def to_paginated_dict(query, page, per_page, api_endpoint, **kwargs):
        resources = query.paginate(page, per_page, error_out=False)

        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(api_endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(api_endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(api_endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }

        return data

class UserRelations(db.Model):
    """
    This relation defines the follower-followed relation between the users.
    """
    __tablename__ = 'user_relations'
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)

class User(db.Model, PaginatedAPI):
    """
    Defines the User relation which contains information about users
    on the surf central platform.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, nullable = False)
    password_hash = db.Column(db.String(128), nullable = False)
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)

    posts = db.relationship('Post', backref='author')

    # followers = db.relationship('User',secondary='user_relations',
    #     primaryjoin=(UserRelations.followed_id==id))
    followed = db.relationship(
        'User', secondary='user_relations',
        primaryjoin=(UserRelations.follower_id == id),
        secondaryjoin=(UserRelations.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        """ User object representation """
        return "<User: {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """ Generates profile image link for new users using gravatar"""
        digest = md5(self.username.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=retro&s={}".format(digest,size)

    def is_following(self, username):
        user_obj = User.query.filter_by(username=username).first()
        follower = UserRelations.query.filter_by(follower_id=self.id,followed_id=user_obj.id).first()
        if follower is None:
            return False
        else:
            return True

    def follow(self, user):
        if not self.is_following(user):
            user_obj = User.query.filter_by(username=user).first()
            relation = UserRelation(follower_id=self.id, followed_id=user_obj.id)
            db.session.add(relation)
            db.commit()
            flash("You have successfully followed {}".format(user))

    def unfollow(self, user):
        if self.is_following(user):
            user_obj = User.query.filter_by(username=user).first()
            UserRelations.query.filter_by(follower_id=self.id, followed_id=user_obj.id).delete()
            db.commit()
            flash("You have unfollowed {}".format(user))

    def get_posts(self):
        posts = Post.query.filter_by(author_id=self.id).order_by(Post.created.desc()).all()
        return posts

    def get_followers(self):
        """
        Return a list of UserRelations objects with the followed_id as the
        current user id, and the follower_id of users who are following the
        current user.
        Note: Currently does not return list of ID's of the followers, but returns
        list of UserRelations.
        """
        follower_users = UserRelations.query.filter_by(followed_id=self.id).all()
        return follower_users

    def get_followed(self):
        """
        Return a list of UserRelations objects with the follower_id as the
        current user id, and the followed_id of users who are being followed by
        the current user.
        Note: Currently does not return list of ID's of the followed users,but
        returns list of UserRelations.
        """
        followed_users = UserRelations.query.filter_by(follower_id=self.id).all()
        return followed_users

    def to_dict(self):
        """
        Function to return meta-data about user in JSON format
        """
        data = {
            'id':self.id,
            'username' : self.username,
            'post_count' : len(self.get_posts()),
            'follower_count' : len(self.get_followers()),
            'followed_count' : len(self.get_followed()),
            'about_me': self.about_me,
            'last_seen': self.last_seen.isoformat(),
            '_links' : {
                    'self' : url_for('api.get_user',id=self.id),
                    'followers' : url_for('api.get_followers',id=self.id),
                    'followed' : url_for('api.get_followed', id=self.id)
            }
        }

        return data

    def from_dict(self, dict_data, new_user=False):
        for field in ['username','about_me']:
            if field in dict_data:
                setattr(self,field,dict_data[field])

        if new_user and 'password' in dict_data:
            self.set_password(dict_data['password'])



class Post(db.Model):
    """
    Defines the post relation which contains information about posts by users
    on the surf central platform.
    """
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key = True)
    created = db.Column(db.DateTime, default = datetime.utcnow)
    title = db.Column(db.String(64), nullable = False)
    body = db.Column(db.String(280), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))


    def __repr__(self):
        return "<Post: {}>".format(self.title)
