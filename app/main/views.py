from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .. import db
from..models import User

@main.route('/', methods=['GET', 'POST'])
def index():
	#session.permanent = True
	return render_template('index.html')

@main.route('/todo', methods=['GET', 'POST'])
def todo():
	return render_template('todolists.html')

@main.route('/user/<username>')
def user(username):
	user = user.query.filter_by(username=username).first()
	if user == None:
		abort()

	return render_template('user.html', user=user)
