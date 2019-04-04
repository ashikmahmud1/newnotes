from flask import Flask

# MongoEngine
from mongoengine import connect
from flask_mongoengine import MongoEngine
from flask_ckeditor import CKEditor
import os

app = Flask(__name__)

# Often people will also separate these into a separate config.py file
app.config['CKEDITOR_SERVE_LOCAL'] = True
app.config['CKEDITOR_HEIGHT'] = 400
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.abspath(__file__))+'/uploads'


# Connect with the mongodb database
connect(
    'newnotesone',
    username='',
    password='',
    host='mongodb://localhost:27017/newnotesone',
    port=27017
)

db = MongoEngine(app)
ckeditor = CKEditor(app)

# Grab the blueprints from the other views.py files for each "app"
from newnotes.students.views import students_blueprint
from newnotes.teachers.views import teachers_blueprint
from newnotes.files.views import files_blueprint
from newnotes.forums.views import forums_blueprint
from newnotes.schools.views import schools_blueprint
from newnotes.assignments.views import assignments_blueprint


app.register_blueprint(students_blueprint, url_prefix="/students")
app.register_blueprint(teachers_blueprint, url_prefix="/teachers")
app.register_blueprint(files_blueprint, url_prefix="/files")
app.register_blueprint(forums_blueprint, url_prefix='/forums')
app.register_blueprint(schools_blueprint, url_prefix='/schools')
app.register_blueprint(assignments_blueprint, url_prefix='/assignments')
