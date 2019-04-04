from flask import Blueprint, render_template, request, session, redirect, url_for
from newnotes.models import Post
from newnotes.forums.forms import QuestionForm
from newnotes.forums.forms import ReplyForm
from newnotes.models import User, Comment

forums_blueprint = Blueprint('forums',
                             __name__,
                             template_folder='templates/forums')


# CRUD FOR THE QUESTION
@forums_blueprint.route('/questions', methods=['GET', 'POST'])
def questions():
    if session.get('email'):
        # get the logged in user by session.get('email')
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            # get all the question from the Post table and send to the view
            posts = Post.objects()
        else:
            return redirect(url_for('students.profile'))
        return render_template('questions.html', posts=posts, user=user)
    else:
        return redirect(url_for('login'))


@forums_blueprint.route('/questions/add', methods=['GET', 'POST'])
def create_question():
    # get the logged in user by session.get('email')
    if session.get('email'):
        form = QuestionForm(request.form)
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            if request.method == 'POST' and form.validate():
                # First save the Question
                post = Post()
                post.subject = form.subject.data
                post.description = form.description.data
                post.author = user.name + ' ' + user.surname
                # After saving question we will get the id of the question
                post.save()
                # Finally in the user Post List Push the id of the question
                user.posts.append(post.id)
                user.save()
                # redirect the user in the questions routes
                return redirect(url_for('forums.questions'))
        else:
            return redirect(url_for('students.profile'))
        return render_template('add-question.html', form=form, user=user)
    else:
        return redirect(url_for('login'))


@forums_blueprint.route('/questions/details/<question_id>', methods=['GET', 'POST'])
def question_details(question_id):
    if session.get('email'):
        # get the logged in user by session.get('email')
        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            # Here get the question by the question id from the database
            question = Post.objects(id=question_id).first()
            # Also populate all the reply in the question
            question_comments = Post.objects(comments__in=question.comments)
            comments = []
            for q in question_comments:
                comments = q.comments
        else:
            return redirect(url_for('students.profile'))

        return render_template('question-details.html', question=question, comments=comments, user=user)
    else:
        return redirect(url_for('login'))


# CRUD FOR THE REPLY
@forums_blueprint.route('/questions/reply/<question_id>', methods=['GET', 'POST'])
def question_reply(question_id):
    if session.get('email'):
        # get the logged in user by session.get('email')

        user = User.objects().filter(email=session.get('email')).first()
        if user.user_type == 'instructor' or user.user_type == 'admin':
            # Here get the question by question id from the database and pass to the view
            question = Post.objects(id=question_id).first()
            form = ReplyForm(request.form)
            form.questionId.data = question.id
            if request.method == 'POST' and form.validate():
                comment = Comment()
                comment.author = user.name + ' ' + user.surname
                comment.description = form.description.data
                comment.post = question.id
                comment.save()
                question.comments.append(comment.id)
                question.save()
                return redirect('/forums/questions/details/' + str(form.questionId.data))
        else:
            return redirect(url_for('students.profile'))
        return render_template('question-reply.html', form=form, question=question, user=user)
    else:
        return redirect(url_for('login'))


@forums_blueprint.route('/reply/remove/<comment_id>', methods=['GET', 'POST'])
def remove_reply(comment_id):
    if session.get('email'):
        question_id = request.args.get('question_id')
        question = Post.objects(id=question_id).first()
        comment = Comment.objects(id=comment_id).first()
        # remove the comment from the database
        # question.comments.remove(comment.id)
        new_comments = list(filter(lambda x: x.id != comment.id, question.comments))
        question.comments = new_comments
        question.save()
        comment.delete()
        # also remove the comment from the question comment array
        return redirect(url_for('forums.question_details', question_id=question_id))
    else:
        return redirect(url_for('login'))


@forums_blueprint.route('/question/remove/<question_id>', methods=['GET', 'POST'])
def remove_question(question_id):
    if session.get('email'):
        user = User.objects().filter(email=session.get('email')).first()
        question = Post.objects(id=question_id).first()
        comments = Comment.objects(post=question.id)
        # remove the comment from the database
        # question.comments.remove(comment.id)
        new_user_posts = list(filter(lambda x: x.id != question.id, user.posts))
        user.posts = new_user_posts
        user.save()
        question.delete()
        comments.delete()
        # also remove the comment from the question comment array
        return redirect(url_for('forums.questions'))
    else:
        return redirect(url_for('login'))
