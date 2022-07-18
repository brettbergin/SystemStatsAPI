#!/usr/bin/env python3

import datetime

from flask import request
from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required

from api.extensions import db
from api.config import Config
from api.models.cpu import CPU

config = Config()

CPUInfoPrint = Blueprint("cpu_print", __name__, url_prefix="/api/cpu")


@CPUInfoPrint.route("/info", methods=["POST"])
@jwt_required()
def cpu_info():
    try:
        if not "cpu_data" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: cpu_data"}), 400
        
        if not "target" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: target"}), 400

        if not "report_id" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: report_id"}), 400

        report_id = request.json["report_id"]
        cpu_data = request.json["cpu_data"]
        target = request.json["target"]

        percents = []
        for cpu_id, cpu_percent in cpu_data.items():
            percents.append(f"{cpu_id}:{cpu_percent}")
    
        record = CPU(
            target=target,
            report_id=report_id,
            timestamp=datetime.datetime.now(),
            percents=", ".join(percents),
        )

        db.session.add(record)
        db.session.commit()

        return jsonify({"msg": "Successfully uploaded cpu info."}), 200

    except Exception as err:
        config.log.error(f"Unable to provide CPU information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide CPU information"})


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
