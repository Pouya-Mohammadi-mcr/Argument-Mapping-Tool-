import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from AMT.Database import Database

bp = Blueprint('Auth', __name__, url_prefix='/Auth')

@bp.route("/signUp", methods=('GET', 'POST'))
def signUp():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        if not Database().register(username,password):
            error = "Username already exists"
        else:
            session['username'] = username
            flash('logged in')
            return redirect(url_for('Auth.signIn'))
        flash(error)

    return render_template('Auth/SignUp.html', error=error)
    

@bp.route('/signIn', methods=('GET', 'POST'))
def signIn():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        if not Database().findUser(username): 
            error = 'Incorrect username'
        elif not Database().matchPassword(username,password): 
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['username'] = username
            return redirect(url_for('Auth.signIn'))

        flash(error)

    return render_template('Auth/SignIn.html', error=error)

@bp.before_app_request
def load_logged_in_user():
    username = session.get('username')

    if username is None:
        g.user = None
    else:
        g.user = Database().findUser(username) 
        print (g.user['username'])

@bp.route('/signOut')
def signOut():
    session.clear()
    return redirect(url_for('Auth.signIn'))

def loginRequired(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

