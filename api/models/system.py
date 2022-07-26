#!/usr/bin/env python3

import uuid

from api.extensions import db


class SystemUser(db.Model):
    __tablename__ = "system_users"

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    report_id = db.Column(db.String(36), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    started = db.Column(db.DateTime, nullable=False)
    terminal = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<SystemUser {self.id}>"

    def obj_to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "report_id": self.report_id,
            "target": self.target,
            "started": self.started,
            "terminal": self.terminal,
            "username": self.username,

        }

class SystemUptime(db.Model):
    __tablename__ = "system_uptime"

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    report_id = db.Column(db.String(36), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    uptime = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<SystemUptime {self.id}>"

    def obj_to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "report_id": self.report_id,
            "target": self.target,
            "uptime": self.uptime,
        }

class SystemOper(db.Model):
    __tablename__ = "operating_system"

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    report_id = db.Column(db.String(36), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    opersys = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<SystemOper {self.id}>"

    def obj_to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "report_id": self.report_id,
            "target": self.target,
            "opersys": self.opersys,
        }
