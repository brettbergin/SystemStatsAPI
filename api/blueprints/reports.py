#!/usr/bin/env python3

import uuid
import datetime

from flask import abort
from flask import request
from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import cross_origin

from api.extensions import db
from api.config import Config
from api.models.reports import UserReports
from api.models.users import User
from api.models.disk  import Disk
from api.models.cpu import CPU
from api.models.process import Process
from api.models.memory import Memory
from api.models.network import NetworkInfo
from api.models.network import NetworkIp
from api.models.system import SystemOper, SystemUptime, SystemUser


config = Config()

ReportsBluePrint = Blueprint("report_print", __name__, url_prefix="/api/report")

@ReportsBluePrint.route("/list", methods=["GET"])
@cross_origin()
@jwt_required()
def list_reports():
    try:
        report_info = UserReports.query.all()
        serialized_report_info = [n.obj_to_dict() for n in report_info]
        return jsonify(serialized_report_info), 200

    except Exception as err:
        config.log.error(f"Unable to provide a reports list. Error: {err}.")
        return jsonify({"error_message": "Unable to provide a reports list."}), 500


@ReportsBluePrint.route("/details", methods=["GET"])
def report_details():
    try:
        report_id = request.args["report_id"]

        user_report = UserReports.query.filter_by(report_id=report_id).first()
        if not user_report:
            return abort(404)

        disk_data = Disk.query.filter_by(report_id=report_id).all()
        serialized_disk_info = [n.obj_to_dict() for n in disk_data]

        cpu_data = CPU.query.filter_by(report_id=report_id).all()
        serialized_cpu_info = [n.obj_to_dict() for n in cpu_data]

        memory_data = Memory.query.filter_by(report_id=report_id).all()
        serialized_memory_info = [n.obj_to_dict() for n in memory_data]

        network_info_data = NetworkInfo.query.filter_by(report_id=report_id).all()
        serialized_network_info_info = [n.obj_to_dict() for n in network_info_data]

        network_ip_data = NetworkIp.query.filter_by(report_id=report_id).all()
        serialized_network_ip_info = [n.obj_to_dict() for n in network_ip_data]

        system_uptime_data = SystemUptime.query.filter_by(report_id=report_id).all()
        serialized_system_uptime_info = [n.obj_to_dict() for n in system_uptime_data]

        system_user_data = SystemUser.query.filter_by(report_id=report_id).all()
        serialized_system_user_info = [n.obj_to_dict() for n in system_user_data]

        system_os_data = SystemOper.query.filter_by(report_id=report_id).all()
        serialized_system_os_info = [n.obj_to_dict() for n in system_os_data]

        process_data = Process.query.filter_by(report_id=report_id).all()
        serialized_process_info = [n.obj_to_dict() for n in process_data]

        response = {
            "disk": serialized_disk_info,
            "cpu": serialized_cpu_info,
            "memory": serialized_memory_info,
            "network_info": serialized_network_info_info,
            "network_ip": serialized_network_ip_info,
            "system_uptime": serialized_system_uptime_info,
            "system_user": serialized_system_user_info,
            "system_os": serialized_system_os_info,
            "processes": serialized_process_info
        }
        return jsonify(response), 200

    except Exception as err:
        config.log.error(f"Unable to provide report details. Error: {err}.")
        return jsonify({"error_message": "Unable to provide report details."}), 500


@ReportsBluePrint.route("/new", methods=["POST"])
@jwt_required()
def create_new_report():
    try:
        current_user = get_jwt_identity()
        this_user = User.query.filter(User.email == current_user).first()

        if not this_user:
            config.log.error(
                f"Unable to find a user in the database that is attempting to register a new report. Error: {err}."
            )
            return (
                jsonify({"error_message": "Unable to create a new user report."}),
                400,
            )

        if not "target" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: target"}), 400

        target = request.json["target"]
        report_id = uuid.uuid4()
        report_id = str(report_id)

        record = UserReports(
            timestamp=datetime.datetime.now(),
            report_id=report_id,
            user_id=this_user.id,
            email=current_user,
            target=target,
        )

        db.session.add(record)
        db.session.commit()

        return jsonify({"report_id": f"{record.report_id}"}), 200

    except Exception as err:
        config.log.error(f"Unable to create a new report. Error: {err}.")
        return jsonify({"error_message": "Unable to register a new report."}), 500
