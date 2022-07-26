#!/usr/bin/env python3

import uuid

from api.extensions import db


class CPU(db.Model):
    __tablename__ = "cpu"

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    report_id = db.Column(db.String(36), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    percents = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<CPU {self.id}>"

    def obj_to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "report_id": self.report_id,
            "target": self.target,
            "percents": self.percents,
        }
