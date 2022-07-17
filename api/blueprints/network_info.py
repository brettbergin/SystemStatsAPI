#!/usr/bin/env python3

import datetime

from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required

# from SysAgent.SysAgentCore.network import NetworkInfoCore

from api.extensions import db
from api.config import Config
from api.models.network import NetworkInfo
from api.models.network import NetworkIp


config = Config()
# psutil_network_info = NetworkInfoCore(config)

NetworkInfoPrint = Blueprint("network_print", __name__, url_prefix="/api/network")


@NetworkInfoPrint.route("/hostname", methods=["GET"])
@jwt_required()
def hostname():
    try:
        # hostname = psutil_network_info.hostname()
        # return jsonify({"hostname": hostname}), 200

        return jsonify({"hostname": []}), 200

    except Exception as err:
        config.log.error(f"Unable to provide hostname information. Error: {err}.")
        return jsonify({"error": "Unable to provide hostname information"}), 500


@NetworkInfoPrint.route("/ip", methods=["GET"])
@jwt_required()
def ip_address():
    try:

        # ip, target = psutil_network_info.ip_address()

        # ips = []
        # for interface in ip['interfaces']:
        #     for k, v in interface.items():
        #         ips.append(f"{k}:{v}")

        # record = NetworkIp(
        #     target=target,
        #     timestamp=datetime.datetime.now(),
        #     addresses=", ".join(ips)
        # )

        # db.session.add(record)
        # db.session.commit()

        # return jsonify({"ip_addresses": ip}), 200
        return jsonify({"ip_addresses": []}), 200

    except Exception as err:
        config.log.error(f"Unable to provide IP information. Error: {err}")
        return jsonify({"error": "Unable to provide IP information"}), 500


@NetworkInfoPrint.route("/info", methods=["GET"])
@jwt_required()
def network_info():
    try:
        # network_data, target = psutil_network_info.net_data()
        # record = NetworkInfo(
        #     target=target,
        #     timestamp=datetime.datetime.now(),
        #     bytes_sent = network_data['bytes_sent'],
        #     bytes_recvd = network_data['bytes_recvd'],
        #     packets_sent = network_data['packets_sent'],
        #     packets_recvd = network_data['packets_recvd'],
        #     err_pkt_in = network_data['err_pkt_in'],
        #     err_pkt_out = network_data['err_pkt_out'],
        #     dropped_pkt_in = network_data['dropped_pkt_in'],
        #     dropped_pkt_out = network_data['dropped_pkt_out'],
        # )
        # db.session.add(record)
        # db.session.commit()
        # return jsonify({"network_info": network_data}), 200
        return jsonify({"network_info": []}), 200

    except Exception as err:
        config.log.error(f"Unable to provide network information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide network information."}), 500
