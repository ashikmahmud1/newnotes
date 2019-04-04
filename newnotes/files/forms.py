from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField
from wtforms.validators import DataRequired, InputRequired


class UploadForm(FlaskForm):
    file = FileField('file', validators=[DataRequired()])
    submit = SubmitField('Upload')


class TagForm(FlaskForm):
    tags = StringField('Tags', validators=[InputRequired()])
    submit = SubmitField('Add')
