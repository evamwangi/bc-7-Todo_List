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

	
class AnonymousUser(AnonymousUserMixin):
	"""for unregistered user"""
	def can(self, permissions):
		return False
# login_manager.anonymous_user = AnonymousUser
		
		

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

class Role(db.Model):
	"""creating roles for the users"""
	__tablename__ = "roles"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			self.role = Role.query.filter_by(default=True).first()

	def can(self,permissions):
		return self.role is not None and\
			(self.role.permissions & permissions) == permissions

	@staticmethod
	def insert_roles():
		roles = {
			'user': (Permission.FOLLOW|
					Permission.WRITE_ARTICLES|
					Permission.COMMENT, True)
		}

		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.Permissions = roles[r][0]
			role.default = roles[r][1]
			db.session.add(role)
		db.session.commit()
		

class Permission:
	FOLLOW = 0x01
	COMMENT = 0x02
	WRITE_ARTICLES = 0x04
	