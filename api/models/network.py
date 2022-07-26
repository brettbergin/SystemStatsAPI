#!/usr/bin/env python3

import uuid

from api.extensions import db


class NetworkInfo(db.Model):
    __tablename__ = "network_info"

    id = db.Column(db.String(36), default=lambda: str(uuid.uuid4()), primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    report_id = db.Column(db.String(36), nullable=False)
    target = db.Column(db.String(255), nullable=False)
    bytes_sent = db.Column(db.String(20), nullable=False)
    bytes_recvd = db.Column(db.String(20), nullable=False)
    packets_sent = db.Column(db.String(20), nullable=False)
    packets_recvd = db.Column(db.String(20), nullable=False)
    err_pkt_in = db.Column(db.String(20), nullable=False)
    err_pkt_out = db.Column(db.String(20), nullable=False)
    dropped_pkt_in = db.Column(db.String(20), nullable=False)
    dropped_pkt_out = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"<NetworkInfo {self.id}>"

    def obj_to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "report_id": self.report_id,
            "target": self.target,
            "bytes_sent": self.bytes_sent,
            "bytes_recvd": self.bytes_recvd,
            "packets_sent": self.packets_sent,
            "packets_recvd": self.packets_recvd,
            "err_pkt_in": self.err_pkt_in,
            "err_pkt_out": self.err_pkt_out,
            "dropped_pkt_in": self.dropped_pkt_in,
            "dropped_pkt_out": self.dropped_pkt_out,
        }


class NetworkIp(db.Model):
    __tablename__ = "network_ips"

    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.String(36), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    target = db.Column(db.String(255), nullable=False)
    addresses = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<NetworkIp {self.id}>"

    def obj_to_dict(self):
        return {
            "id": self.id,
            "report_id": self.report_id,
            "timestamp": self.timestamp,
            "target": self.target,
            "addresses": self.addresses,
        }
