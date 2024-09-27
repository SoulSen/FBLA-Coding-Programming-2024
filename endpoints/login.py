from flask import request, jsonify, render_template, make_response, redirect
from flask.views import MethodView
from flask_jwt_extended import set_access_cookies

from models.user import User


class Login(MethodView):
    def get(self):
        return render_template('login.html', flash_message=False)

    def post(self):
        data = request.form

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if (not username and not email) or not password:
            return render_template('login.html', flash_message=True)

        if username:
            user = User.query.filter_by(
                username=username
            ).first()
        elif email:
            user = User.query.filter_by(
                email=email
            ).first()

        if not user:
            return render_template('login.html', flash_message=True)

        pwd_check = user.check_password(password)

        if not user or not pwd_check:
            response = {
                'status': 'fail',
                'message': 'user or password incorrect'
            }

            return render_template('login.html', flash_message=True), 404

        token = user.create_jwt_token()

        response = make_response(redirect('/'))

        set_access_cookies(response, token)
        return response, 200
