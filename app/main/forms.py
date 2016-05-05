from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required


class TodoForm(Form):
    todo= TextField('', validators=[Required()])
    description = TextField('description', validators=[Required()])
    submit = SubmitField('Add')