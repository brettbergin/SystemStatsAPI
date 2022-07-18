#!/usr/bin/env python3

import datetime

from flask import request
from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required


from api.extensions import db
from api.config import Config
from api.models.disk import Disk

config = Config()

DiskInfoPrint = Blueprint("disk_print", __name__, url_prefix="/api/disk")


@DiskInfoPrint.route("/info", methods=["POST"])
@jwt_required()
def disk_info():
    try:
        if not "disk_data" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: disk_data"}), 400
        
        if not "target" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: target"}), 400

        if not "report_id" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: report_id"}), 400

        report_id = request.json["report_id"]
        disk_data = request.json["disk_data"]
        target = request.json["target"]

        for disk in disk_data:
            record = Disk(
                target=target,
                report_id=report_id,
                timestamp=datetime.datetime.now(),
                mount_point = disk['mount_point'],
                total = disk['total'],
                used = disk['used'],
                free = disk['free'],
                percent = disk['percent']
            )
            db.session.add(record)
        db.session.commit()

        return jsonify({"msg": "Successfully uploaded disk info."}), 200

    except Exception as err:
        config.log.error(f"Unable to provide disk information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide disk information."}), 500
