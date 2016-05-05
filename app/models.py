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
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	name = db.Column(db.String(64))
	location = db.Column(db.String(64))
	about_me = db.Column(db.Text())
	member_since = db.Column(db.DateTime(), default=datetime.utcnow)
	last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

	
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

	def ping(self):
		self.last_seen = datetime.utcnow()
		db.session.add(self)

class Todo():
	__tablename__ = 'todo_list'

	id = db.Column(db.Integer, primary_key=True)
	todo = db.Column(db.String(64), index=True)
	description = db.Column(db.String(64), index=True)


	

	@login_manager.user_loader
	def load_user(user_id):
		'''	
			Is a Flask-Login callback function.
			It loads a user, given the identifier.
		'''
		return User.query.get(int(user_id))

