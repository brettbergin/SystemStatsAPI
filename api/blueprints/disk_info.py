#!/usr/bin/env python3

import datetime

from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required

# from SysAgent.SysAgentCore.disk import DiskInfo

from api.extensions import db
from api.config import Config
from api.models.disk import Disk

config = Config()
# psutil_disk_info = DiskInfo(config)

DiskInfoPrint = Blueprint("disk_print", __name__, url_prefix="/api/disk")


@DiskInfoPrint.route("/info", methods=["GET"])
@jwt_required()
def disk_info():
    try:
        # disk_data, target = psutil_disk_info.partitions()
        # for disk in disk_data:
        #     record = Disk(
        #         target=target,
        #         timestamp=datetime.datetime.now(),
        #         mount_point = disk['mount_point'],
        #         total = disk['total'],
        #         used = disk['used'],
        #         free = disk['free'],
        #         percent = disk['percent']
        #     )
        #     db.session.add(record)
        # db.session.commit()

        # return jsonify({"disk_info": disk_data}), 200
        return jsonify({"disk_info": []}), 200

    except Exception as err:
        config.log.error(f"Unable to provide disk information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide disk information."}), 500
