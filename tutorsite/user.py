import functools
import re
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from tutorsite.db import get_db

user = Blueprint('user', __name__, url_prefix='/user')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))
        return view(**kwargs)
    return wrapped_view

@user.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

@user.route('register', methods=('GET', 'POST'))
def register():
    if g.user is not None:
        return redirect(url_for('post.index'))
    elif request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        db = get_db()
        error = None
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        if not re.search(regex, email):
            error = 'Invalid email address.'
        elif db.execute('SELECT id FROM user WHERE email = ?', (email,)).fetchone():
            error = 'Email is already in use.'
        elif len(username) < 6:
            error = 'Username must be at least 6 characters.'
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,)).fetchone():
            error = 'Username is already in use.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters.'
        elif confirm != password:
            error = 'Confirm password is incorrect.'

        if error is None:
            db.execute(
                'INSERT INTO user (email, username, password) VALUES (?,?,?)',
                (email, username, generate_password_hash(password))
            )
            db.commit()

            session.clear()
            user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
            session['user_id'] = user['id']

            return redirect(url_for('post.index'))
        
        flash(error)
    
    return render_template('user/register.html')

@user.route('login', methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect(url_for('post.index'))
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()

        if user is None:
            error = 'User not found.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('post.index'))
        
        flash(error)
    
    return render_template('user/login.html')

@user.route('logout')
def logout():
    session.clear()
    return redirect(url_for('post.index'))

# maybe make it so that user can edit there acc from here?
@user.route('account')
@login_required
def account():
    #
    #
    return render_template('user/account.html')

#@user.route('<username>/account')
#@login_required
#def otheruser(username):
#    db = get_db()
#    user = db.execute('SELECT * FROM user WHERE username = ?',(username,)).fetchone()
#    posts = db.execute('SELECT * FROM post WHERE author_id = ?',(user['author_id'],))
#   return #render_template('user/otheruser.html', posts=posts, user=user)