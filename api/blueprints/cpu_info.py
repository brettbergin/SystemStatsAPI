#!/usr/bin/env python3

import datetime

from flask import request
from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required

from api.extensions import db
from api.config import Config
from api.models.cpu import CPU
from api.models.process import Process


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


@CPUInfoPrint.route("/processes", methods=["POST"])
@jwt_required()
def process_info():
    try:
        if not "process_data" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: process_data"}), 400
        
        if not "target" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: target"}), 400

        if not "report_id" in request.json.keys():
            return jsonify({"msg": "Missing request parameter: report_id"}), 400

        process_data = request.json["process_data"]
        report_id = request.json["report_id"]
        target = request.json["target"]

        for process in process_data:
            proc_name = process.get("name")
            proc_pid = process.get("pid")
            proc_user = process.get("user")
            proc_status = process.get("status")
            proc_create_time = process.get("create_time")
            proc_exe = process.get("executable")
            proc_cpu_percent = process.get("cpu_percent")

            open_files = ", ".join([p.__str__() for p in process["open_files"]]) \
                if process.get("open_files") \
                else None
        
            connections = ", ".join([p.__str__() for p in process["connections"]]) \
                if process.get("connections") \
                else None
        
            threads = ", ".join([p.__str__() for p in process["threads"]]) \
                if process.get("threads") \
                else None

            mem_info = ", ".join(str(process["mem_info"])) \
                if process.get("mem_info") \
                else None

            cli = ", ".join(process["cli"]) \
                if process.get("cli") \
                else None

            existing_process = Process.query.filter(
                Process.name==proc_name, 
                Process.pid==proc_pid, 
                Process.user==proc_user
            ).first()

            if not existing_process:
                new_process = Process(
                    target=target,
                    report_id=report_id,
                    timestamp=datetime.datetime.now(),
                    name=proc_name,
                    pid=proc_pid,
                    user=proc_user,
                    status=proc_status,
                    create_time=proc_create_time,
                    cli=cli,
                    executable=proc_exe,
                    cpu_percent=proc_cpu_percent,
                    mem_info=mem_info,
                    open_files=open_files,
                    connections=connections,
                    threads=threads
                )
                db.session.add(new_process)
            else:
                existing_process.name = proc_name
                existing_process.pid = proc_pid
                existing_process.user = proc_user
                existing_process.status = proc_status
                existing_process.create_time = proc_create_time
                existing_process.cli = cli
                existing_process.executable = proc_exe
                existing_process.cpu_percent = proc_cpu_percent
                existing_process.mem_info = mem_info
                existing_process.open_files = open_files
                existing_process.connections = connections
                existing_process.threads = threads
                db.session.commit()

        db.session.commit()

        return jsonify({"msg": "Successfully uploaded process info."}), 200

    except Exception as err:
        config.log.error(f"Unable to provide Process information. Error: {err}.")
        return jsonify({"error_message": "Unable to provide Process information"}), 500
