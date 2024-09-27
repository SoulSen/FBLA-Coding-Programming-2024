import datetime

from flask_jwt_extended import create_access_token
from passlib.handlers.pbkdf2 import pbkdf2_sha512

from models import db


class User(db.Model):
    __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String, unique=False, nullable=False)
    last_name = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    codes = db.relationship('ResetCode', backref='user')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = pbkdf2_sha512.hash(password)

    @staticmethod
    def get_user(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def add_user(first_name, last_name, email, password):
        if User.query.filter_by(email=email):
            return False

        user = User(first_name, last_name, email, password)
        user.save()

        return True

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        user.delete()

        return True

    def create_jwt_token(self):
        token = create_access_token(identity=self.id, expires_delta=datetime.timedelta(days=2))

        return token

    def check_password(self, pwd):
        return pbkdf2_sha512.verify(pwd, self.password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def as_dict(self):
        return {
            'user_id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }

    def __repr__(self):
        return f"<User: Username - {self.username}>"
