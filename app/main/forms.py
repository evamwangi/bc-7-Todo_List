from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextField
from wtforms.validators import Required
from werkzeug.datastructures import MultiDict


class TodoForm(Form):
    todos = StringField('todoList', validators=[Required()]) 
											 
    description = StringField('description', validators=[Required()])
    
    submit = SubmitField('submit')

    