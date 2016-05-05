from datetime import datetime
from flask import render_template, session, redirect, url_for
from flask.ext.login import login_required
from flask.ext.login import current_user
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
	if form.validate_on_submit():
		todo_list = Todo(todos=form.todos.data, description=form.description.data, author=current_user._get_current_object())
		# flash('added to the list.')
		db.session.add(todo_list)
		db.session.commit()
	todo = Todo.query.all()
	return render_template('todolists.html', form=form, todo=todo)

@main.route('/user/<username>')
def user(username):
	user = user.query.filter_by(username=username).first()
	if user == None:
		abort()

	return render_template('user.html', user=user)
