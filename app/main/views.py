from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask.ext.login import login_required
from . import main
from .. import db
from..models import User, Todo
from . forms import TodoForm

@main.route('/', methods=['GET', 'POST'])
def index():
	#session.permanent = True
	return render_template('index.html')

@main.route('/todo', methods=['GET', 'POST'])

@login_required
def todo():
	form = TodoForm()
	Todo(todolists= form.todo.data, description=form.description.data)
	if todo is not None :
			return redirect(url_for('main.todo'))
		flash('added to the list.')
	return render_template('todolists.html')

@main.route('/user/<username>')
def user(username):
	user = user.query.filter_by(username=username).first()
	if user == None:
		abort()

	return render_template('user.html', user=user)
