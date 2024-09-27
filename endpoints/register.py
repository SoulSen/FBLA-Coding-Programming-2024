from flask import request, jsonify, make_response, render_template, redirect
from flask.views import MethodView

from models.user import User


class Register(MethodView):
    def get(self):
        return render_template('register.html', flash_message=False)

    def post(self):
        data = request.form

        user = User.query.filter_by(email=data.get('email')).first()

        if user:
            return render_template('register.html', flash_message=True)

        user = User(
            first_name=data.get('firstName'),
            last_name=data.get('lastName'),
            email=data.get('email'),
            password=data.get('password')
        )

        user.save()

        response = {
            'status': 'success',
            'message': 'successfully registered',
        }

        return redirect("login"), 201
