from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from tutorsite.user import login_required
from tutorsite.db import get_db

post = Blueprint('post', __name__)

@post.route('/')
def index():
    # sends the posts variable to the browser, which shows all posts in order
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
        # information to create a new post
        title = request.form['title']
        body = request.form['body']
        db = get_db()
        error = None

        #error checking
        if len(title) < 4:
            error = 'Title must be at least 4 characters.'
        elif len(title) > 50:
            error = 'Title must be at most 50 characters.'
        elif len(body) < 10:
            error = 'Body must be at least 10 characters.'

        if error is None:
            # inserts new post into database
            db.execute(
                'INSERT INTO post (title, body, author_id) VALUES (?,?,?)',
                (title, body, g.user['id'])
            )
            db.execute('UPDATE user SET elixir = ? WHERE id = ?', (g.user['elixir'] + 10, g.user['id'])) # adds elixer to user account
            db.commit()

            return redirect(url_for('post.index'))

        flash(error)

    return render_template('post/create.html')

@post.route('/<int:id>/comments')
def comments(id):
    # shows all comments for a certain post
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
        # new comment information
        body = request.form['body']
        db = get_db()
        error = None

        # error checking
        if len(body) < 10:
            error = 'Comment must be at least 10 characters.'

        if error is None:
            # inserts new comment to database
            db.execute('INSERT INTO comment (body, author_id, post_id) VALUES (?,?,?)', (body, g.user['id'], id))
            db.execute('UPDATE user SET elixir = ? WHERE id = ?', (g.user['elixir'] + 5, g.user['id']))
            db.commit()

            return redirect(url_for('post.comments', id=id))

        flash(error)

    return render_template('post/newcomment.html')

# not related to posts but we put it here anyway
@post.route('/calculator', methods=('GET', 'POST'))
def calculator():
    if request.method == 'POST':
        # calculator information
        metrics = request.form['metrics']
        weight = request.form['weight']
        height = request.form['height']
        error = None

        try:
            weight = float(weight)
            height = float(height)

            if metrics == 'inches and pounds':
                bmi =  float((weight*703)/(height**2))
            else: 
                bmi = float(weight/(height**2))
            
            if bmi >= 18.5 and bmi <= 24.9:
                advice = 'Your body mass index ratio is healthy. Keep up the good work and continue the healthy habits!'
            elif bmi < 18.5:
                advice = 'You are a underweight. You should try eating foods with more nutrients and carbohydrates.'
            elif bmi >= 25 and bmi <= 29.9:
                advice = 'You are a overweight. You should try to get more physical activity or start a light diet.'
            else: 
                advice = 'You are obese. You should consult with your doctor about a healthier lifestyle ASAP. Obesity can cause to serious, and often life-threatening, health issues.'

        except Exception:
            error = 'Your weight and height are not valid.'

        if error is None:
            return render_template('calculator.html', bmi=round(bmi, 1), advice=advice)

        flash(error)

    return render_template('calculator.html')