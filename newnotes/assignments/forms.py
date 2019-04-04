from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, DateField, FileField
from wtforms.validators import DataRequired, InputRequired


class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    description = CKEditorField('Body', validators=[DataRequired()])
    submission_date = DateField('Submission Date', format='%m/%d/%Y', validators=[InputRequired()])
    submit = SubmitField('Submit')


class AssignmentDocumentForm(FlaskForm):
    file = FileField('file', validators=[DataRequired()])
    submit = SubmitField('Upload')
