from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort
from tutorsite.user import login_required
from tutorsite.db import get_db

post = Blueprint('post', __name__)

@post.route('/')
def index():
    #db = get_db()
    #posts = db.execute(
    #    'SELECT p.id, title, body, created, author_id, username'
    #    ' FROM post p JOIN user u ON p.author_id = u.id'
    #    ' ORDER BY created DESC'
    #).fetchall()
    return render_template('post/index.html')#, posts=posts)