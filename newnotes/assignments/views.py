import os
from flask import Blueprint, render_template, request, session, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from newnotes import app

from newnotes.assignments.forms import AssignmentForm, AssignmentDocumentForm
from newnotes.models import User, Assignment, School, Document

assignments_blueprint = Blueprint('assignments',
                                  __name__,
                                  template_folder='templates/assignments')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'pptx', 'docx', 'mp4'}


# Only instructor and admin can access this route
@assignments_blueprint.route('/', methods=['GET', 'POST'])
def assignment_list():
    if session.get('email'):
        # get the logged in user by session.get('email')
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            # get all the question from the Post table and send to the view
            assignments = Assignment.objects(school=user.school.id)
        else:
            return redirect(url_for('students.profile'))
        return render_template('assignments.html', assignments=assignments, user=user)
    else:
        return redirect(url_for('login'))


# Only instructor and admin can access this route
@assignments_blueprint.route('/details/<assignment_id>', methods=['GET', 'POST'])
def assignment_details(assignment_id):
    if session.get('email'):
        # get the logged in user by session.get('email')
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            # get all the question from the Post table and send to the view
            assignment = Assignment.objects(id=assignment_id).first()
        else:
            return redirect(url_for('students.profile'))
        return render_template('assignment-details.html', assignment=assignment, user=user)
    else:
        return redirect(url_for('login'))


# Only instructor and admin can access this route
@assignments_blueprint.route('/create', methods=['GET', 'POST'])
def create_assignment():
    # get the logged in user by session.get('email')
    if session.get('email'):
        form = AssignmentForm(request.form)
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            if request.method == 'POST' and form.validate():
                # First save the Question
                assignment = Assignment()
                assignment.title = form.title.data
                assignment.description = form.description.data
                assignment.submission_date = form.submission_date.data
                assignment.created_by = user.id
                assignment.school = user.school.id
                assignment.save()
                # get the user school
                user_school = School.objects(id=user.school.id).first()
                user_school.assignments.append(assignment.id)
                # After saving question we will get the id of the question
                # Finally in the user Post List Push the id of the question
                user_school.save()
                # redirect the user in the questions routes
                return redirect(url_for('assignments.assignment_list'))
        else:
            return redirect(url_for('students.profile'))
        return render_template('assignment-create.html', form=form, user=user)
    else:
        return redirect(url_for('login'))


# only student can access this route
# This is for student for uploading document in an assignment
@assignments_blueprint.route('/document/<assignment_id>', methods=['GET', 'POST'])
def upload_document(assignment_id):
    # get the logged in user by session.get('email')
    if session.get('email'):
        submitted = False
        assignment = Assignment.objects(id=assignment_id).first()
        # check if the user is already submitted the assignment document or not
        form = AssignmentDocumentForm()
        user = User.objects().filter(email=session.get('email')).first()
        previously_submitted_doc = Document.objects(assignment=assignment.id, submitted_by=user.id).first()
        if previously_submitted_doc is not None:
            submitted = True
            form.submit.label.text = 'Edit Upload'
        if request.method == 'POST' and form.validate():
            file = form.file.data
            if file and allowed_file(file.filename):
                if not submitted:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    # save the file name in the database
                    document = Document()
                    document.filename = filename
                    document.assignment = assignment.id
                    document.submitted_by = user.id
                    document.save()
                    # push the document id in the assignment documents array
                    assignment.documents.append(document.id)
                    assignment.save()
                    # set a flash message that document successfully updated
                else:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    previously_submitted_doc.filename = filename
                    previously_submitted_doc.save()
                    # set a flash message that document successfully updated
            # redirect the user in the questions routes
            return redirect(url_for('assignments.assignment_list'))
        return render_template('assignment-document.html', form=form, assignment=assignment, user=user,
                               submitted=submitted, document=previously_submitted_doc)
    else:
        return redirect(url_for('login'))


@assignments_blueprint.route('/close/<assignment_id>', methods=['GET', 'POST'])
def close_assignment(assignment_id):
    if session.get('email'):
        # get the logged in user by session.get('email')
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            # get all the question from the Post table and send to the view
            assignment = Assignment.objects(id=assignment_id).first()
            # make the assignment status false
            assignment.status = False
            assignment.save()
        return redirect(url_for('assignments.assignment_details', assignment_id=assignment_id))
    else:
        return redirect(url_for('login'))


@assignments_blueprint.route('/open/<assignment_id>', methods=['GET', 'POST'])
def open_assignment(assignment_id):
    if session.get('email'):
        # get the logged in user by session.get('email')
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            # get all the question from the Post table and send to the view
            assignment = Assignment.objects(id=assignment_id).first()
            # make the assignment status True
            assignment.status = True
            assignment.save()
        return redirect(url_for('assignments.assignment_details', assignment_id=assignment_id))
    else:
        return redirect(url_for('login'))


# Checking if the file uploaded is in the allowed extension variable
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@assignments_blueprint.route('/download/<file_name>', methods=['GET', 'POST'])
def download(file_name):
    uploads = app.config['UPLOAD_FOLDER']
    return send_from_directory(directory=uploads, filename=file_name)
