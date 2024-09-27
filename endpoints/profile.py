from flask import render_template, redirect
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.user import User


class Profile(MethodView):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()

        user = User.get_user(user_id)

        user_info = user.as_dict()

        if user_id:
            return render_template('profile.html',
                                   first_name=user_info['first_name'], last_name=user_info['last_name'],
                                   email=user_info['email'], flash_message=False)
        else:
            return redirect("/login")
