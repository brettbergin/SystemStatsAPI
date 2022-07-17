#!/usr/bin/env python3

import os
import secrets

from api.logger import Logger


class Config(object):
    def __init__(self):
        self.flask_debug = True if os.environ['FLASK_DEBUG'].lower() == "development" else False
        self.log_level = "DEBUG" if self.flask_debug == True else "INFO"
        
        self.flask_host = "127.0.0.1"
        self.flask_port = 5000

        self.flask_app_secret = secrets.token_hex()
        self.flask_jwt_secret = secrets.token_hex()

        self.flask_test_user = os.environ["SYSAGENT_TEST_USER"] if os.environ.get("SYSAGENT_TEST_USER") else "test@test.com"
        self.flask_test_passwd = os.environ["SYSAGENT_TEST_PASSWD"] if os.environ.get("SYSAGENT_TEST_PASSWD") else "test"

        self.rate_limit_frequency = "50000/day;2500/hour;100/minute"

        self.db_host = os.environ["SYSAGENT_DB_HOST"] if os.environ.get("SYSAGENT_DB_HOST") else "localhost"
        self.db_port = os.environ["SYSAGENT_DB_PORT"] if os.environ.get("SYSAGENT_DB_PORT") else 3306
        self.db_username = os.environ["SYSAGENT_DB_USERNAME"] if os.environ.get("SYSAGENT_DB_USERNAME") else "test"
        self.db_password = os.environ["SYSAGENT_DB_PASSWORD"] if os.environ.get("SYSAGENT_DB_PASSWORD") else "testtest"
        self.db_name = os.environ["SYSAGENT_DB_NAME"]if os.environ.get("SYSAGENT_DB_NAME") else "sysagent"

        self.log = Logger(self.log_level).setup_logging()
