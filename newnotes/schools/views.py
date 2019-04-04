from flask import Blueprint, render_template, session, redirect, url_for, send_from_directory, request, flash
from newnotes.models import File, User, School, Chat, Module1, Module2, Module3
from newnotes.schools.forms import ChatForm
from newnotes import app

schools_blueprint = Blueprint('schools',
                              __name__,
                              template_folder='templates/schools')


# Module1
@schools_blueprint.route('/module1', methods=['GET', 'POST'])
def module1():
    # Check if the user logged in or not. if not logged in then redirect to login
    if session.get('email'):
        user = User.objects().filter(email=session.get('email')).first()
        # check if the user is teacher or if student then also check if the student is approved or not
        if (user.user_type == 'instructor' or user.approved) or user.user_type == 'admin':
            user_school = School.objects(id=user.school.id).first()
            files = user_school.module1.files
            print(files)
            # Here Fetch All the user school chat
            chats = user_school.module1.chats
            chats.sort(key=lambda x: x['created_at'], reverse=True)
            # sort the order of the chat by created_at
            return render_template('module1.html', files=files, user=user, chats=chats)
    else:
        return redirect(url_for('login'))


# Module2
@schools_blueprint.route('/module2', methods=['GET', 'POST'])
def module2():
    # Check if the user logged in or not. if not logged in then redirect to login
    if session.get('email'):
        user = User.objects().filter(email=session.get('email')).first()
        # check if the user is teacher or if student then also check if the student is approved or not
        if (user.user_type == 'instructor' or user.approved) or user.user_type == 'admin':
            user_school = School.objects(id=user.school.id).first()
            files = user_school.module2.files
            # Here Fetch All the user school chat
            chats = user_school.module2.chats
            chats.sort(key=lambda x: x['created_at'], reverse=True)
            return render_template('module2.html', files=files, user=user, chats=chats)
    else:
        return redirect(url_for('login'))


# Module3
@schools_blueprint.route('/module3', methods=['GET', 'POST'])
def module3():
    # Check if the user logged in or not. if not logged in then redirect to login
    if session.get('email'):
        user = User.objects().filter(email=session.get('email')).first()
        # check if the user is teacher or if student then also check if the student is approved or not
        if (user.user_type == 'instructor' or user.approved) or user.user_type == 'admin':
            user_school = School.objects(id=user.school.id).first()
            files = user_school.module3.files
            # Here Fetch All the user school chat
            chats = user_school.module3.chats
            chats.sort(key=lambda x: x['created_at'], reverse=True)
            return render_template('module3.html', files=files, user=user, chats=chats)
    else:
        redirect(url_for('login'))


# Only Instructor Have Access to This Route
@schools_blueprint.route('/chat_create/<module>', methods=['GET', 'POST'])
def chat_create(module):
    if session.get('email'):
        form = ChatForm(request.form)
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            if request.method == 'POST' and form.validate():
                # save the chat and it will return id of that chat
                chat = Chat()
                chat.user = user.id
                chat.description = form.description.data
                chat.save()
                user_school = School.objects(id=user.school.id).first()
                # finally push the id of the chat in the user_school module
                if module == 'module1':
                    flash('Chat Successfully Added to Module1 !')
                    # get the module 1 by it's user_school module1
                    user_school_module1 = Module1.objects(id=user_school.module1.id).first()
                    user_school_module1.chats.append(chat.id)
                    user_school_module1.save()
                elif module == 'module2':
                    flash('Chat Successfully Added to Module2 !')
                    user_school_module2 = Module2.objects(id=user_school.module2.id).first()
                    user_school_module2.chats.append(chat.id)
                    user_school_module2.save()
                elif module == 'module3':
                    flash('Chat Successfully Added to Module3 !')
                    user_school_module3 = Module3.objects(id=user_school.module3.id).first()
                    user_school_module3.chats.append(chat.id)
                    user_school_module3.save()
                # save the user_school
                user_school.save()
                # Finally redirect the user to the chat-create
                # With a Flash Message that Chat Successfully Created
                return redirect(url_for('schools.chat_create', module=module))
        else:
            return redirect(url_for('students.profile'))
        return render_template('chat-create.html', form=form, user=user, module=module)
    else:
        return redirect(url_for('login'))


@schools_blueprint.route('/add_to_module1/<file_id>', methods=['GET', 'POST'])
def add_to_module1(file_id):
    # Check if the user logged in or not. if not logged in then redirect to login
    if session.get('email'):
        file = File.objects(id=file_id).first()
        # get the logged in user school
        # finally add the file to the module1 array
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            user_school = School.objects(id=user.school.id).first()
            user_school_module1 = Module1.objects(id=user_school.module1.id).first()
            user_school_module1.files.append(file.id)
            user_school_module1.save()
            return redirect(url_for('files.file_list'))
    else:
        return redirect(url_for('login'))


@schools_blueprint.route('/add_to_module2/<file_id>', methods=['GET', 'POST'])
def add_to_module2(file_id):
    # Check if the user logged in or not. if not logged in then redirect to login
    if session.get('email'):
        file = File.objects(id=file_id).first()
        # get the logged in user school
        # finally add the file to the module1 array
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            user_school = School.objects(id=user.school.id).first()
            user_school_module2 = Module2.objects(id=user_school.module2.id).first()
            user_school_module2.files.append(file.id)
            user_school_module2.save()
            return redirect(url_for('files.file_list'))
    else:
        return redirect(url_for('login'))


@schools_blueprint.route('/add_to_module3/<file_id>', methods=['GET', 'POST'])
def add_to_module3(file_id):
    # Check if the user logged in or not. if not logged in then redirect to login
    if session.get('email'):
        file = File.objects(id=file_id).first()
        # get the logged in user school
        # finally add the file to the module1 array
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            user_school = School.objects(id=user.school.id).first()
            user_school_module3 = Module3.objects(id=user_school.module3.id).first()
            user_school_module3.files.append(file.id)
            user_school_module3.save()
            return redirect(url_for('files.file_list'))
    else:
        return redirect(url_for('login'))


@schools_blueprint.route('/download/<file_name>', methods=['GET', 'POST'])
def download(file_name):
    uploads = app.config['UPLOAD_FOLDER']
    return send_from_directory(directory=uploads, filename=file_name)
