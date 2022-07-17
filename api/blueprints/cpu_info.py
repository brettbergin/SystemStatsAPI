#!/usr/bin/env python3

import datetime

from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required

# from SysAgent.SysAgentCore.cpu import CPUInfo

from api.extensions import db
from api.config import Config
from api.models.cpu import CPU

config = Config()
# psutil_cpu_info = CPUInfo(config)

CPUInfoPrint = Blueprint("cpu_print", __name__, url_prefix="/api/cpu")


@CPUInfoPrint.route("/info", methods=["GET"])
@jwt_required()
def cpu_info():
    try:
        # cpu_data, target = psutil_cpu_info.cpu_data()
        
        # percents=[]
        # for cpu_id, cpu_percent in cpu_data.items():
        #     percents.append(f"{cpu_id}:{cpu_percent}")
    
        # record = CPU(
        #     target=target,
        #     timestamp=datetime.datetime.now(),
        #     percents=", ".join(percents),
        # )

        # db.session.add(record)
        # db.session.commit()

        # return jsonify({"cpu_info": cpu_data}), 200
        return jsonify({"cpu_info": []}), 200

    except Exception as err:
        config.log.error(f"Unable to provide CPU information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide CPU information"}), 500


@CPUInfoPrint.route("/processes", methods=["GET"])
@jwt_required()
def process_info():
    try:
        # process_data = psutil_cpu_info.processes()
        # return jsonify({"process_info": process_data}), 200
        
        return jsonify({"process_info": []}), 200

    except Exception as err:
        config.log.error(f"Unable to provide process information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide process information"}), 500
