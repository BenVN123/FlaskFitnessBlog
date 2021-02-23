from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from tutorsite.user import login_required
from tutorsite.db import get_db

post = Blueprint('post', __name__)

@post.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('post/index.html', posts=posts)

@post.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        db = get_db()
        error = None

        if len(title) < 4:
            error = 'Title must be at least 4 characters.'
        elif len(title) > 50:
            error = 'Title must be at most 50 characters.'
        elif len(body) < 10:
            error = 'Body must be at least 10 characters.'

        if error is None:
            db.execute(
                'INSERT INTO post (title, body, author_id) VALUES (?,?,?)',
                (title, body, g.user['id'])
            )
            db.commit()

            return redirect(url_for('post.index'))

        flash(error)

    return render_template('post/create.html')

@post.route('/<int:id>/comments')
def comments(id):
    db = get_db()
    post = db.execute('SELECT * FROM post WHERE id = ?', (id,)).fetchone()
    username = db.execute('SELECT * FROM user WHERE id = ?', (post['author_id'],)).fetchone()
    comments = db.execute(
        'SELECT c.id, body, created, author_id, post_id, username'
        ' FROM comment c JOIN user u ON c.author_id = u.id WHERE post_id = ?'
        ' ORDER BY created DESC', (id,)
    ).fetchall()

    return render_template('post/comments.html', post=post, comments=comments, username=username['username'])

@post.route('/<int:id>/newcomment', methods=('GET', 'POST'))
@login_required
def newcomment(id):
    if request.method == 'POST':
        body = request.form['body']
        db = get_db()
        error = None

        if len(body) < 10:
            error = 'Comment must be at least 10 characters.'

        if error is None:
            db.execute(
                'INSERT INTO comment (body, author_id, post_id) VALUES (?,?,?)',
                (body, g.user['id'], id)
            )
            db.commit()

            return redirect(url_for('post.comments', id=id))

        flash(error)

    return render_template('post/newcomment.html')
