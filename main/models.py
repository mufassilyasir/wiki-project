from flask import Blueprint
from flask_login import UserMixin
from flask_security import RoleMixin
from . import db

models = Blueprint("models", __name__, static_folder="static", template_folder="templates")


class Roles(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    def __str__(self):
        return self.name

role_user = db.Table('role_user',
db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
db.Column('user_type', db.Text))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    roles = db.relationship('Roles', secondary=role_user, backref=db.backref('users', lazy='select'))

    def __str__(self):
        return self.name
    
    def has_role(self, *args):
        return set(args).issubset({role.id for role in self.roles})
    
class WikiPages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.Text)
    title = db.Column(db.Text)
    updated_at = db.Column(db.Text)
    html = db.Column(db.Text)
    admin_only = db.Column(db.Integer)
    category = db.Column(db.Integer)

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.Text)
    
class Faqs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answer = db.Column(db.Text)