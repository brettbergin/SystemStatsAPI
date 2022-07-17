#!/usr/bin/env python3

import datetime
from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required

# from SysAgent.SysAgentCore.memory import MemoryInfo

from api.extensions import db
from api.config import Config
from api.models.memory import Memory


config = Config()
# psutil_memory_info = MemoryInfo(config)

MemoryInfoPrint = Blueprint("memory_print", __name__, url_prefix="/api/memory")


@MemoryInfoPrint.route("/info", methods=["GET"])
@jwt_required()
def memory_info_route():
    try:
        # mem_data, target = psutil_memory_info.mem_data()
        # record = Memory(
        #     active=mem_data['active'],
        #     target=target,
        #     timestamp=datetime.datetime.now(),
        #     available=mem_data['available_memory'],
        #     free=mem_data['free'],
        #     inactive=mem_data['inactive'],
        #     percent=mem_data['percent'],
        #     total=mem_data['total_memory'],
        #     used=mem_data['used'],
        #     wired=mem_data['wired']
        # )
        # db.session.add(record)
        # db.session.commit()

        # return jsonify({"memory_info": mem_data}), 200
        return jsonify({"memory_info": []}), 200

    except Exception as err:
        config.log.error(f"Unable to provide memory information. Error: {err}.")
        return jsonify({"error": f"Unable to provide memory information."}), 500
