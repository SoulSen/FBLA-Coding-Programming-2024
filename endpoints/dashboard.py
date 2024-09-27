from flask import render_template, redirect
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.partner import Partner
from models.user import User


class Dashboard(MethodView):
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()

        user = User.get_user(user_id)

        user_info = user.as_dict()

        if user_id:
            return render_template('dashboard.html', partners=Partner.get_partners(),
                                   first_name=user_info['first_name'], last_name=user_info['last_name'],
                                   community_count=Partner.community_partner_count(),
                                   business_count=Partner.business_partner_count())
        else:
            return redirect("/login")
