#!/usr/bin/env python3

import datetime

from flask import request
from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

from api.extensions import db
from api.config import Config
from api.models.system import SystemUser
from api.models.system import SystemUptime
from api.models.system import SystemOper


config = Config()

SystemInfoPrint = Blueprint("system_print", __name__, url_prefix="/api/system")

@SystemInfoPrint.route("/users/list", methods=["GET"])
@cross_origin()
@jwt_required()
def fetch_system_user_list():
    try:
        users_info = SystemUser.query.all()
        serialized_users_info = [n.obj_to_dict() for n in users_info]
        return jsonify(serialized_users_info), 200

    except Exception as err:
        config.log.error(f"Unable to provide users information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide users information"})


@SystemInfoPrint.route("/os", methods=["POST"])
@jwt_required()
def operating_system():
    try:
        if not "os" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: os"}), 400

        if not "target" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: target"}), 400

        if not "report_id" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: report_id"}), 400

        report_id = request.json["report_id"]
        operating_system = request.json["os"]
        target = request.json["target"]

        record = SystemOper(
            target=target,
            report_id=report_id,
            timestamp=datetime.datetime.now(),
            opersys=operating_system,
        )

        db.session.add(record)
        db.session.commit()

        return jsonify({"msg": "Successfully uploaded operating system info."}), 200

    except Exception as err:
        config.log.error(
            f"Unable to provide operating system information. Error: {err}."
        )
        return jsonify({"error": "Unable to provide operating system information"}), 500


@SystemInfoPrint.route("/uptime", methods=["POST"])
@jwt_required()
def up_time():
    try:
        if not "uptime" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: uptime"}), 400

        if not "target" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: target"}), 400

        if not "report_id" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: report_id"}), 400

        report_id = request.json["report_id"]
        uptime = request.json["uptime"]
        target = request.json["target"]

        record = SystemUptime(
            target=target,
            report_id=report_id,
            timestamp=datetime.datetime.now(),
            uptime=uptime,
        )

        db.session.add(record)
        db.session.commit()

        return jsonify({"msg": "Successfully uploaded uptime info."}), 200

    except Exception as err:
        config.log.error(f"Unable to provide uptime information. Error: {err}.")
        return jsonify({"error": "Unable to provide uptime information"}), 500


@SystemInfoPrint.route("/users", methods=["POST"])
@jwt_required()
def user_info():
    try:
        if not "users" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: users"}), 400

        if not "target" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: target"}), 400

        if not "report_id" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: report_id"}), 400

        report_id = request.json["report_id"]
        users = request.json["users"]
        target = request.json["target"]

        for user in users:
            record = SystemUser(
                target=target,
                report_id=report_id,
                timestamp=datetime.datetime.now(),
                started=user["started"],
                terminal=user["terminal"],
                username=user["user_name"],
            )

            db.session.add(record)

        db.session.commit()

        return jsonify({"msg": "Successfully uploaded users info."}), 200

    except Exception as err:
        config.log.error(f"Unable to provide user information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide user information."}), 500
