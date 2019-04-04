from newnotes import db
from datetime import datetime


# Hash Password storing field will be a BinaryField

# for student we should make another model
# since student has some additional field than teacher
class School(db.Document):
    name = db.StringField(required=True, max_length=100)
    # Below method will not work anymore
    # Since Now Module will have both files and chats reference
    # So we should create separate model for module1, module2, module3
    # module1 = db.ListField(db.ReferenceField('File'))
    # module2 = db.ListField(db.ReferenceField('File'))
    # module3 = db.ListField(db.ReferenceField('File'))
    # chats = db.ListField(db.ReferenceField('Chat'))

    module1 = db.ReferenceField('Module1')
    module2 = db.ReferenceField('Module2')
    module3 = db.ReferenceField('Module3')
    # A school will have a list of assignment
    assignments = db.ListField(db.ReferenceField('Assignment'))
    meta = {
        'collection': 'schools'
    }


class Assignment(db.Document):
    title = db.StringField(required=True, max_length=200)
    description = db.StringField()
    # who is created this assignment. that means the reference of the user
    created_by = db.ReferenceField('User')
    # which school belongs to this assignment.
    school = db.ReferenceField('School')
    # Assignment will have a submission date
    submission_date = db.DateTimeField(required=True)
    # Assignment will have a status open or close. true means open false means close
    status = db.BooleanField(required=True, default=True)
    # An assignment will have a list of document which we can call documents
    documents = db.ListField(db.ReferenceField('Document'))
    meta = {
        'collection': 'assignments'
    }


class Document(db.Document):
    # name of the file
    filename = db.StringField()
    # which assignment this document belongs to
    assignment = db.ReferenceField('Assignment')
    # who is submitted the document
    submitted_by = db.ReferenceField('User')
    # when submitted the document
    submitted_date = db.DateTimeField(required=True, default=datetime.utcnow)
    meta = {
        'collection': 'documents'
    }


class Module1(db.Document):
    files = db.ListField(db.ReferenceField('File'))
    chats = db.ListField(db.ReferenceField('Chat'))
    meta = {
        'collection': 'module1'
    }


class Module2(db.Document):
    files = db.ListField(db.ReferenceField('File'))
    chats = db.ListField(db.ReferenceField('Chat'))
    meta = {
        'collection': 'module2'
    }


class Module3(db.Document):
    files = db.ListField(db.ReferenceField('File'))
    chats = db.ListField(db.ReferenceField('Chat'))
    meta = {
        'collection': 'module3'
    }


class Chat(db.Document):
    description = db.StringField(required=True)
    # A user reference who is added this chat
    user = db.ReferenceField('User')
    created_at = db.DateTimeField(required=True, default=datetime.utcnow)
    meta = {
        'collection': 'chats'
    }


class User(db.DynamicDocument):
    # We can make the title field optional. because only teachers have a title
    # student table we should keep some additional field dl_docs_array and login_counter and login_array
    # All this field will be set dynamically
    dl_docs_array = db.ListField(db.ReferenceField('File'))
    login_counter = db.IntField()
    login_array = db.ListField(db.DateField())
    title = db.StringField()
    approved = db.BooleanField()

    name = db.StringField(required=True, max_length=50)
    surname = db.StringField(required=True)
    email = db.EmailField(required=True)
    password = db.BinaryField(required=True)
    user_type = db.StringField(required=True)
    school = db.ReferenceField(School)  # Here will store id of the school
    # Here will be list of post collection
    posts = db.ListField(db.ReferenceField('Post'))

    meta = {
        'collection': 'users'
    }


class File(db.Document):
    user = db.ReferenceField('User')
    filename = db.StringField()
    tags = db.ListField(db.StringField(), default=list)
    created_at = db.DateTimeField(required=True, default=datetime.utcnow)
    meta = {
        'collection': 'files'
    }


class Post(db.Document):
    subject = db.StringField()
    author = db.StringField(required=True, max_length=50)
    description = db.StringField()
    created_at = db.DateTimeField(required=True, default=datetime.utcnow)
    comments = db.ListField(db.ReferenceField('Comment'))
    # Post will have a list of comments
    meta = {
        'collection': 'posts'
    }


# keep a post field in the comment which will make to find or delete the comment very easily
class Comment(db.DynamicDocument):
    description = db.StringField()
    post = db.ReferenceField('Post')
    created_at = db.DateTimeField(required=True, default=datetime.utcnow)
    user_id = db.ReferenceField(User)  # here will store id of the user
    author = db.StringField(required=True, max_length=50)
    meta = {
        'collection': 'comments'
    }
