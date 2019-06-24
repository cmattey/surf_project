from flask import (
    Blueprint, url_for, render_template, g, flash, redirect, request, session
    )
from werkzeug.exceptions import abort
from surf_app.auth import login_required
from surf_app.models import User,Post,UserRelations
from surf_app import db, app

bp = Blueprint('blog', __name__)

@bp.route('/')
def landing_page():
    if 'user_id' in session:
        return redirect(url_for('blog.index'))
    else:
        return render_template('blog/landing_page.html')


@bp.route('/home')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    posts = g.user.get_followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'],error_out=False)

    next_url = url_for('blog.index',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('blog.index',page=posts.prev_num) if posts.has_prev else None

    return render_template('blog/index.html', posts = posts.items,
        next_url = next_url, prev_url = prev_url)

@bp.route('/explore')
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created.desc()).paginate(page,
        app.config['POSTS_PER_PAGE'], error_out = False)

    next_url = url_for('blog.explore',page=posts.next_num) if posts.has_next else None
    prev_url = url_for('blog.explore',page=posts.prev_num) if posts.has_prev else None

    return render_template('blog/explore.html', posts = posts.items,
        next_url = next_url, prev_url = prev_url)

@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    if request.method=='POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'
        elif not body:
            error = 'Body is required'

        if error is not None:
            flash(error)
        else:
            post = Post(title=title, body=body, author_id=g.user.id)

            db.session.add(post)
            db.session.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

# The check_author argument is defined so that the function can be used to get
# a post without checking the author. This would be useful if you wrote a view
# to show an individual post on a page, where the user doesn’t matter because
# they’re not modifying the post.
def get_post(id, check_author = True):
    post = Post.query.filter_by(id=id).first()

    if post is None:
        abort(404,"Post id {0} doesn't exist".format(id))
    if check_author and post.author.id != g.user.id:
        abort(403,"Forbidden, You do not have access to this resource")
    return post


@bp.route('/<int:id>/update', methods=('GET','POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method=='POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if title is None:
            error = "Title is required"
        elif body is None:
            error = "Body is required"

        if error is not None:
            flash(error)
        else:
            old_post = Post.query.filter_by(id=id).first()
            old_post.title = title
            old_post.body = body
            db.session.commit()
        return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post = post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    Post.query.filter_by(id=id).delete()
    db.session.commit()
    return redirect(url_for('blog.index'))
