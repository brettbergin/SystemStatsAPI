#!/usr/bin/env python3

from datetime import timedelta


from flask import Flask

from api.extensions import db, jwt, rate_limit
from api.config import Config
from api.blueprints.memory_info import MemoryInfoPrint
from api.blueprints.cpu_info import CPUInfoPrint
from api.blueprints.disk_info import DiskInfoPrint
from api.blueprints.network_info import NetworkInfoPrint
from api.blueprints.system_info import SystemInfoPrint
from api.blueprints.base import BasePrint
from api.blueprints.reports import ReportsBluePrint



class InitApp(object):

    def __init__(self):
        self.config = Config()
        
        self.db_url = f"mysql://{self.config.db_username}:{self.config.db_password}@{self.config.db_host}:{self.config.db_port}/{self.config.db_name}"
        
        self.this_app_secret = self.config.flask_app_secret
        self.this_jwt_secret = self.config.flask_jwt_secret
        
        self.rate_limit_strategy = "fixed-window-elastic-expiry"
        self.rate_limit_frequency = "50000/day;2500/hour;100/minute"

        self._internal_app = None

    def _register_extensions(self):
        rate_limit.init_app(self._internal_app)
        jwt.init_app(self._internal_app)
        db.init_app(self._internal_app)

    def _register_blue_prints(self):
        self._internal_app.register_blueprint(MemoryInfoPrint)
        self._internal_app.register_blueprint(CPUInfoPrint)
        self._internal_app.register_blueprint(DiskInfoPrint)
        self._internal_app.register_blueprint(NetworkInfoPrint)
        self._internal_app.register_blueprint(SystemInfoPrint)
        self._internal_app.register_blueprint(BasePrint)
        self._internal_app.register_blueprint(ReportsBluePrint)

    def create_app(self):
        self._internal_app = Flask(__name__)
        self._internal_app.config.from_object(self.config)

        self._internal_app.config["SECRET_KEY"] = self.this_app_secret

        self._internal_app.config["JWT_SECRET_KEY"] = self.this_jwt_secret
        self._internal_app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
        self._internal_app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
        self._internal_app.config["JWT_TOKEN_LOCATION"] = ["headers"]

        self._internal_app.config["RATELIMIT_ENABLED"] = True
        self._internal_app.config["RATELIMIT_HEADERS_ENABLED"] = True
        self._internal_app.config["RATELIMIT_STRATEGY"] = self.rate_limit_strategy
        self._internal_app.config["RATELIMIT_DEFAULT"] = self.rate_limit_frequency

        self._internal_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        self._internal_app.config['SQLALCHEMY_DATABASE_URI'] = self.db_url

        self._register_extensions()
        self._register_blue_prints()

        return self._internal_app