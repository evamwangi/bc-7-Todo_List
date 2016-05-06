from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin, AnonymousUserMixin
from flask.ext.login import UserMixin
from app import db, login_manager
from datetime import datetime

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	# confirmed = db.Column(db.Boolean, default = False)

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	todos = db.relationship('Todo', backref='author', lazy='dynamic')

	
	@property 
	def password(self):
		'''
		'''
		raise AttributeError('password cannot be read (write-only attribute)')

	@password.setter
	def password(self, password):
		'''
		'''
		self.password_hash = generate_password_hash(password)


	def verify_password(self, password):
		"""
		function verifies the password
		"""
		return check_password_hash(self.password_hash, password)

	# def __init__(self, username, email):
	# 	self.username = username
	#  	self.email = email

	#  def __repr__(self):
	# 	return '<User %r>' self.username


class Todo(db.Model):
	__tablename__ = 'todo_list'

	id = db.Column(db.Integer, primary_key=True)
	todos = db.Column(db.String(64), index=True)
	description = db.Column(db.String(64), index=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	done = db.Column(db.Boolean(), default=False)
	author_id = db.Column(db.Integer, db.ForeignKey('users.id'))


	

	@login_manager.user_loader
	def load_user(user_id):
		'''	
			Is a Flask-Login callback function.
			It loads a user, given the identifier.
		'''
		return User.query.get(int(user_id))

		