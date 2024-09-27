from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.user import User


class UserInfo(MethodView):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.get_user(user_id)

        user_info = user.as_dict()
        user_info['status'] = 'success'

        return jsonify(user_info)
