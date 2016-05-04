from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
	__tablename__ = 'users'
	# confirmed = db.Column(db.Boolean, default = False)

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	email = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))

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
		'''
		'''
		return check_password_hash(self.password_hash, password)

	# def generate_confirmation_token(self, expiration=3600):
	# 	s = Serializer(current_app.config['SECRET_KEY'], expiration)
	# 	return s.dumps({'confirm': self.id})

	# def confirm(self, token):
	# 	s = Serializer(current_app.config['SECRET_KEY'])
	# 	try:
	# 		s.loads(token)
	# 	except:
	# 		return False
	# 	if data.get('confirm') != self.id:
	# 		return False

	# 	self.confirm = True
	# 	db.session.add(self)
	# 	return True


	@login_manager.user_loader
	def load_user(user_id):
		'''	
			Is a Flask-Login callback function.
			It loads a user, given the identifier.
		'''
		return User.query.get(int(user_id))

	