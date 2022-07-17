#!/usr/bin/env python3

import datetime

from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required

# from SysAgent.SysAgentCore.system import SystemInfo

from api.extensions import db
from api.config import Config
from api.models.system import SystemUser
from api.models.system import SystemUptime
from api.models.system import SystemOper


config = Config()
# psutil_system_info = SystemInfo(config)

SystemInfoPrint = Blueprint("system_print", __name__, url_prefix="/api/system")


@SystemInfoPrint.route("/os", methods=["GET"])
@jwt_required()
def operating_system():
    try:
        # operating_system, target = psutil_system_info.operating_system()
        # record = SystemOper(
        #     target=target,
        #     timestamp=datetime.datetime.now(),
        #     opersys=operating_system
        # )
        
        # db.session.add(record)
        # db.session.commit()

        # return jsonify({"operating_system": operating_system}), 200
        return jsonify({"operating_system": []}), 200

    except Exception as err:
        config.log.error(
            f"Unable to provide operating system information. Error: {err}."
        )
        return jsonify({"error": "Unable to provide operating system information"}), 500


@SystemInfoPrint.route("/uptime", methods=["GET"])
@jwt_required()
def up_time():
    try:
        # uptime, target = psutil_system_info.uptime()
        
        # record = SystemUptime(
        #     target=target,
        #     timestamp=datetime.datetime.now(),
        #     uptime=uptime
        # )

        # db.session.add(record)
        # db.session.commit()

        # return jsonify({"uptime": str(uptime)}), 200
        return jsonify({"uptime": []}), 200

    except Exception as err:
        config.log.error(f"Unable to provide uptime information. Error: {err}.")
        return jsonify({"error": "Unable to provide uptime information"}), 500


@SystemInfoPrint.route("/users", methods=["GET"])
@jwt_required()
def user_info():
    try:
        # user_data, target = psutil_system_info.users()
        # for user in user_data:
        #     record = SystemUser(
        #         target=target,
        #         timestamp=datetime.datetime.now(),
        #         started=user['started'],
        #         terminal=user['terminal'],
        #         username=user['user_name']
        #     )

        #     db.session.add(record)

        # db.session.commit()

        # return jsonify({"user_info": user_data}), 200
        return jsonify({"user_info": []}), 200

    except Exception as err:
        config.log.error(f"Unable to provide user information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide user information."}), 500
