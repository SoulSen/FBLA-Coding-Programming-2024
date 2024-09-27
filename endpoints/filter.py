from flask import render_template, redirect, request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.partner import Partner
from models.user import User


class FilterDashboard(MethodView):
    @jwt_required(optional=True)
    def post(self):
        user_id = get_jwt_identity()

        user = User.get_user(user_id)
        user_info = user.as_dict()

        data = request.form
        clean_data = {}

        for key, value in data.items():
            if value != "":
                clean_data[key] = value

        if clean_data == {}:
            partners = Partner.get_partners()
        else:
            partners = Partner.filter_partners(**clean_data)

        if user_id:
            return render_template('dashboard.html', partners=partners,
                                   first_name=user_info['first_name'], last_name=user_info['last_name'],
                                   community_count=Partner.community_partner_count(),
                                   business_count=Partner.business_partner_count())
        else:
            return redirect("/login")
