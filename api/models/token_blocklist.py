#!/usr/bin/env python3

import uuid

from flask_jwt_extended import get_jwt_identity
from sqlalchemy.sql import func


from api.extensions import db
from api.models.users import User


def get_current_user():
    email = get_jwt_identity()
    user = User.query.filter(User.email == email).one_or_none()
    return user


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)
    type = db.Column(db.String(16), nullable=True)

    user_id = db.Column(
        db.ForeignKey("users.id"), default=lambda: get_current_user().id, nullable=False
    )

    def __repr__(self):
        return f"<TokenBlocklist {self.id}>"
