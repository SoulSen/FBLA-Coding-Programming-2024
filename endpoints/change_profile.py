from flask import request, redirect, render_template
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity
from passlib.handlers.pbkdf2 import pbkdf2_sha512

from models.user import User


class ChangeProfile(MethodView):
    @jwt_required(optional=True)
    def post(self):
        user_id = get_jwt_identity()

        user = User.get_user(user_id)

        data = request.form

        email = data.get('email')
        password = data.get('password')

        user.email = email
        user.password = pbkdf2_sha512.hash(password)
        user.save()

        user_info = user.as_dict()

        print('changed')

        return render_template('profile.html',
                               first_name=user_info['first_name'], last_name=user_info['last_name'],
                               email=user_info['email'], flash_message=True)
