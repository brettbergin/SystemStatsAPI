#!/usr/bin/env python3

import uuid

from api.extensions import db


class Memory(db.Model):
    __tablename__ = "memory"

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    report_id = db.Column(db.String(36), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    active = db.Column(db.String(20), nullable=False)
    available = db.Column(db.String(20), nullable=False)
    free = db.Column(db.String(20), nullable=False)
    inactive = db.Column(db.String(20), nullable=False)
    percent = db.Column(db.Integer, nullable=False)
    total = db.Column(db.String(20), nullable=False)
    used = db.Column(db.String(20), nullable=False)
    wired = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<Memory {self.id}>"

    def obj_to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "report_id": self.report_id,
            "target": self.target,
            "active": self.active,
            "available": self.available,
            "free": self.free,
            "inactive": self.inactive,
            "percent": self.percent,
            "total": self.total,
            "user": self.used,
            "wired": self.wired,
        }
