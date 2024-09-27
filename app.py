from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

import models
from config import Config
from endpoints.add_partner import AddPartner
from endpoints.change_password import ChangePassword
from endpoints.change_profile import ChangeProfile
from endpoints.dashboard import Dashboard
from endpoints.filter import FilterDashboard
from endpoints.index import Index
from endpoints.login import Login
from endpoints.logout import Logout
from endpoints.register import Register
from endpoints.remove_partner import RemovePartner
from endpoints.search import SearchDashboard
from endpoints.user_info import UserInfo
from endpoints.profile import Profile


class Server:
    db = models.db
    cors = CORS()
    migrate = Migrate()
    jwt = JWTManager()

    def __init__(self):
        self.app = Flask(__name__)

        self.app.config.from_object(Config)
        self.db.init_app(self.app)
        self.migrate.init_app(self.app)
        self.jwt.init_app(self.app)

        self.register_views()

    def register_views(self):
        login = Login.as_view('login')
        logout = Logout.as_view('logout')
        register = Register.as_view('register')
        user_info = UserInfo.as_view('user-info')
        change_password = ChangePassword.as_view('change-password')
        dashboard = Dashboard.as_view('dashboard')
        add_partner = AddPartner.as_view('add-partner')
        profile = Profile.as_view('profile')
        remove_partner = RemovePartner.as_view('remove-partner')
        filter_dashboard = FilterDashboard.as_view('filter-dashboard')
        search_dashboard = SearchDashboard.as_view('search-dashboard')
        change_profile = ChangeProfile.as_view('change-profile')
        index = Index.as_view('index')

        self.app.add_url_rule('/login', view_func=login)
        self.app.add_url_rule('/logout', view_func=logout)
        self.app.add_url_rule('/register', view_func=register)
        self.app.add_url_rule('/user-info', view_func=user_info)
        self.app.add_url_rule('/change-forget-password', view_func=change_password)
        self.app.add_url_rule('/', view_func=dashboard)
        self.app.add_url_rule('/add-partner', view_func=add_partner)
        self.app.add_url_rule('/profile', view_func=profile)
        self.app.add_url_rule('/remove-partner', view_func=remove_partner)
        self.app.add_url_rule('/filter-dashboard', view_func=filter_dashboard)
        self.app.add_url_rule('/search-dashboard', view_func=search_dashboard)
        self.app.add_url_rule('/change-profile', view_func=change_profile)
        self.app.add_url_rule('/index', view_func=index)

    def setup(self):
        with self.app.app_context():
            self.db.create_all()
        server.app.run(debug=True)


server = Server()
server.setup()
