#!/usr/bin/env python3

import uuid

from api.extensions import db


class UserReports(db.Model):
    __tablename__ = "user_reports"

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"))
    timestamp = db.Column(db.DateTime, nullable=False)
    report_id = db.Column(db.String(36), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    
    def __repr__(self):
        return f"<UserReports {self.id}>"

    def obj_to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "timestamp": self.timestamp,
            "report_id": self.report_id,
            "target": self.target,
            "email": self.email,
        }
