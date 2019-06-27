import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from . import auth, blog, user, api, beaches

app.register_blueprint(auth.bp)
app.register_blueprint(blog.bp)
app.register_blueprint(user.bp)
app.register_blueprint(api.bp)
app.register_blueprint(beaches.bp)
# app.add_url_rule('/',endpoint='index')
