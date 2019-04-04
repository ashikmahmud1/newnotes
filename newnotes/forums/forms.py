from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import InputRequired, DataRequired


class QuestionForm(FlaskForm):
    subject = StringField('Subject', validators=[InputRequired()])
    description = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReplyForm(FlaskForm):
    questionId = HiddenField('Question ID')
    description = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField('Submit')
