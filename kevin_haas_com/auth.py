import requests
from random import getrandbits
from time import sleep
from flask import Response, Blueprint, render_template, redirect, url_for, request, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from flask_app import app, cache, login_manager
from flask_app.models import Account


auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Account.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash('You are not authorized to view that page. Please login.')
    return redirect(url_for('auth.login')), 302

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html'), 200

@auth.route('/register', methods=['GET', 'POST'])
def register():
	return render_template('register.html'), 200

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login')), 302


@auth.route('/hello', methods=['GET', 'POST'])
def hello():
	return 'Hello World', 200

