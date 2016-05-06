from datetime import datetime
from flask import render_template, session, redirect, url_for, request, jsonify
from flask.ext.login import login_required
from flask.ext.login import current_user
from . import main
from .. import db
from..models import User, Todo
from . forms import TodoForm
from flask import flash

@main.route('/', methods=['GET', 'POST'])
def index():
	
	return render_template('index.html')

@main.route('/todo', methods=['GET', 'POST'])
@login_required
def todo():
	form = TodoForm()
	if form.validate_on_submit():
		todo_list = Todo(todos=form.todos.data, description=form.description.data, author=current_user._get_current_object())
		db.session.add(todo_list)
		db.session.commit()
		return redirect(url_for('main.todo'))
	todo = Todo.query.filter_by(done=False).all()
	done = Todo.query.filter_by(done=True).all()
	return render_template('todolists.html', db=db, form=form, todo=todo, done=done)

@main.route('/donetodos' , methods=['GET', 'POST'])
def donetodos():
	data = request.get_json()
	timestamp = data['timestamp']
	todo = Todo.query.filter_by(timestamp=timestamp).first()	
	todo.done = True
	db.session.add(**todo)
	db.session.commit()
	todos = Todo.query.filter_by(done=True).all()
	todos = [{'todos': todo.todos, 'description': todo.description, 'timestamp': todo.timestamp} for todo in todos]

	return jsonify(**{'todos': todos})
	

@main.route('/undo', methods=['GET', 'POST'])
def undo():
	data = request.get_json()
	timestamp = data['timestamp']
	todo = Todo.query.filter_by(timestamp=timestamp).first()	
	todo.done = False
	db.session.add(todo)
	db.session.commit()
	todos = Todo.query.filter_by(done=False).all()
	todos = [{'todos': todo.todos, 'description': todo.description, 'timestamp': todo.timestamp} for todo in todos]

	return jsonify(**{'todos': todos})

@main.route('/user/<username>')
def user(username):
	user = user.query.filter_by(username=username).first()
	if user == None:
		abort()

	return render_template('user.html', user=user)
