#!/usr/bin/env python3

import datetime

from flask import request
from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

from api.extensions import db
from api.config import Config
from api.models.network import NetworkInfo
from api.models.network import NetworkIp


config = Config()

NetworkInfoPrint = Blueprint("network_print", __name__, url_prefix="/api/network")


@NetworkInfoPrint.route("/ip", methods=["POST"])
@jwt_required()
def ip_address():
    try:
        if not "ips" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: ips"}), 400

        if not "target" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: target"}), 400

        if not "report_id" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: report_id"}), 400

        report_id = request.json["report_id"]
        incoming_ips = request.json["ips"]
        target = request.json["target"]

        ips = []
        for interface in incoming_ips["interfaces"]:
            for k, v in interface.items():
                ips.append(f"{k}:{v}")

        record = NetworkIp(
            target=target,
            report_id=report_id,
            timestamp=datetime.datetime.now(),
            addresses=", ".join(ips),
        )

        db.session.add(record)
        db.session.commit()

        return jsonify({"msg": "Successfully uploaded network ips."}), 200

    except Exception as err:
        config.log.error(f"Unable to provide IP information. Error: {err}")
        return jsonify({"error": "Unable to provide IP information"}), 500


@NetworkInfoPrint.route("/list", methods=["GET"])
@cross_origin()
@jwt_required()
def fetch_network_info():
    try:
        network_info = NetworkInfo.query.all()
        serialized_network_info = [n.obj_to_dict() for n in network_info]
        return jsonify(serialized_network_info), 200

    except Exception as err:
        config.log.error(f"Unable to provide network information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide network information"})


@NetworkInfoPrint.route("/info", methods=["POST"])
@jwt_required()
def network_info():
    try:
        if not "network_data" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: network_data"}), 400

        if not "target" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: target"}), 400

        if not "report_id" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: report_id"}), 400

        report_id = request.json["report_id"]
        network_data = request.json["network_data"]
        target = request.json["target"]

        record = NetworkInfo(
            target=target,
            report_id=report_id,
            timestamp=datetime.datetime.now(),
            bytes_sent=network_data["bytes_sent"],
            bytes_recvd=network_data["bytes_recvd"],
            packets_sent=network_data["packets_sent"],
            packets_recvd=network_data["packets_recvd"],
            err_pkt_in=network_data["err_pkt_in"],
            err_pkt_out=network_data["err_pkt_out"],
            dropped_pkt_in=network_data["dropped_pkt_in"],
            dropped_pkt_out=network_data["dropped_pkt_out"],
        )

        db.session.add(record)
        db.session.commit()

        return jsonify({"msg": "Successfully uploaded network info."}), 200

    except Exception as err:
        config.log.error(f"Unable to provide network information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide network information."}), 500
