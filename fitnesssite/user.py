import functools
import re
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from tutorsite.db import get_db

# creates blueprint
user = Blueprint('user', __name__, url_prefix='/user')

# decorator function to make sure user is logged in
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user.login'))
        return view(**kwargs)
    return wrapped_view

# loads user information before every request
@user.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

@user.route('register', methods=('GET', 'POST'))
def register():
    if g.user is not None: # if user is already logged in, redirect to home page
        return redirect(url_for('post.index'))
    elif request.method == 'POST':
        # takes information from request and stores in variables
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm = request.form['confirm']
        db = get_db()
        error = None
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        # makes sure all information is valid
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
            # if the information is all valid, insert that new user into the table user
            db.execute(
                'INSERT INTO user (email, username, password) VALUES (?,?,?)',
                (email, username, generate_password_hash(password))
            )
            db.commit()

            # logs the new user in
            session.clear()
            user = db.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
            session['user_id'] = user['id']

            return redirect(url_for('post.index')) # redirects to home page
        
        flash(error) # flashes error messages if user did not meet criteria above
    
    return render_template('user/register.html') # renders the user/register.html template in the templates/ folder

@user.route('login', methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect(url_for('post.index')) # redirect if logged in
    elif request.method == 'POST':
        # load information from request
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute('SELECT * FROM user WHERE email = ?', (email,)).fetchone()

        # error checking
        if user is None:
            error = 'User not found.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # if there are no errors, load the user to session (logs them in)
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('post.index'))
        
        flash(error)
    
    return render_template('user/login.html')

@user.route('logout')
def logout():
    # clears session, logging the user out
    session.clear()
    return redirect(url_for('post.index'))

@user.route('account')
@login_required
def account():
    db = get_db()
    posts = db.execute('SELECT p.author_id FROM post p JOIN user u ON p.author_id = u.id WHERE u.id = ?', (g.user['id'],)).fetchall()
    comments = db.execute('SELECT c.author_id FROM comment c JOIN user u ON c.author_id = u.id WHERE u.id = ?', (g.user['id'],)).fetchall()

    return render_template('user/account.html', posts=posts, comments=comments)