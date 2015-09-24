from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

class SearchForm(Form):
    street = StringField('street', validators=[DataRequired()])
    number = StringField('number')
    address = StringField('address', validators=[DataRequired()])
