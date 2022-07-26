#!/usr/bin/env python3

import uuid

from api.extensions import db


class Disk(db.Model):
    __tablename__ = "disk"

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    report_id = db.Column(db.String(36), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    mount_point = db.Column(db.String(20), nullable=False)
    total = db.Column(db.String(20), nullable=False)
    used = db.Column(db.String(20), nullable=False)
    free = db.Column(db.String(20), nullable=False)
    percent = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Disk {self.id}>"

    def obj_to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "report_id": self.report_id,
            "target": self.target,
            "mount_point": self.mount_point,
            "total": self.total,
            "used": self.used,
            "free": self.free,
            "percent": self.percent,
        }
