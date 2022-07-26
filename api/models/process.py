#!/usr/bin/env python3

import uuid

from api.extensions import db


class Process(db.Model):
    __tablename__ = "process"

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    report_id = db.Column(db.String(36), nullable=False)
    target = db.Column(db.String(255), nullable=False)

    name = db.Column(db.String(255), nullable=True)
    pid = db.Column(db.String(255), nullable=True)
    user = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    create_time = db.Column(db.DateTime, nullable=True)
    cli = db.Column(db.Text, nullable=True)
    executable = db.Column(db.String(255), nullable=True)
    cpu_percent = db.Column(db.String(255), nullable=True)
    mem_info = db.Column(db.String(255), nullable=True)
    open_files = db.Column(db.Text, nullable=True)
    connections = db.Column(db.Text, nullable=True)
    threads = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Process {self.id}>"

    def obj_to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "report_id": self.report_id,
            "target": self.target,
            "name": self.name,
            "pid": self.pid,
            "user": self.user,
            "status": self.status,
            "create_time": self.create_time,
            "cli": self.cli,
            "executable": self.executable,
            "cpu_percent": self.cpu_percent,
            "mem_info": self.mem_info,
            "open_files": self.open_files,
            "connections": self.connections,
            "threads": self.threads,
        }
