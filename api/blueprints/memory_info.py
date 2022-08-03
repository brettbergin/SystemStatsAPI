#!/usr/bin/env python3

import datetime

from flask import request
from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin

from api.extensions import db
from api.config import Config
from api.models.memory import Memory


config = Config()

MemoryInfoPrint = Blueprint("memory_print", __name__, url_prefix="/api/memory")


@MemoryInfoPrint.route("/list", methods=["GET"])
@cross_origin()
@jwt_required()
def fetch_network_info():
    try:
        memory_info = Memory.query.all()
        serialized_memory_info = [n.obj_to_dict() for n in memory_info]
        return jsonify(serialized_memory_info), 200

    except Exception as err:
        config.log.error(f"Unable to provide memory information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide memory information"})


@MemoryInfoPrint.route("/info", methods=["POST"])
@jwt_required()
def memory_info_route():
    try:
        if not "mem_data" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: mem_data"}), 400

        if not "target" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: target"}), 400

        if not "report_id" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: report_id"}), 400

        report_id = request.json["report_id"]
        mem_data = request.json["mem_data"]
        target = request.json["target"]

        record = Memory(
            active=mem_data["active"],
            target=target,
            report_id=report_id,
            timestamp=datetime.datetime.now(),
            available=mem_data["available_memory"],
            free=mem_data["free"],
            inactive=mem_data["inactive"],
            percent=mem_data["percent"],
            total=mem_data["total_memory"],
            used=mem_data["used"],
            wired=mem_data["wired"],
        )

        db.session.add(record)
        db.session.commit()

        return jsonify({"msg": "Successfully uploaded memory info."}), 200

    except Exception as err:
        config.log.error(f"Unable to provide memory information. Error: {err}.")
        return jsonify({"error": f"Unable to provide memory information."}), 500
