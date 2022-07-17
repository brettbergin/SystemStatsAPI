#!/usr/bin/env python3

from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
jwt = JWTManager()
rate_limit = Limiter(key_func=get_remote_address)
