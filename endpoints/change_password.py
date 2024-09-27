from flask import request, jsonify
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from passlib.handlers.pbkdf2 import pbkdf2_sha512

from models.reset_code import ResetCode
from models.user import User


class ChangePassword(MethodView):
    @jwt_required(optional=True)
    def post(self):
        data = request.get_json()

        email = data.get('email')
        code = data.get('code')
        password = data.get('password')

        if not email:
            return jsonify({"status": "fail", "message": "invalid form"})

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:
            return jsonify({"status": "fail", "message": "email not exist"})

        reset_code = ResetCode.query.filter_by(
            code=code
        ).first()

        other_user = User.query.filter_by(
            id=reset_code.owner_id
        ).first()

        if user != other_user:
            return jsonify({"status": "fail", "message": "something went wrong"})

        user.password = pbkdf2_sha512.hash(password)
        user.save()
        reset_code.delete()

        return jsonify({"status": "success", "message": "password changed"})
