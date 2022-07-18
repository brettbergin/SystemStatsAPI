#!/usr/bin/env python3

import uuid
import datetime

from flask import request
from flask import Blueprint
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.extensions import db
from api.config import Config
from api.models.reports import UserReports
from api.models.users import User

config = Config()

ReportsBluePrint = Blueprint("report_print", __name__, url_prefix="/api/report")


@ReportsBluePrint.route("/new", methods=["POST"])
@jwt_required()
def create_new_report():
    try:
        current_user = get_jwt_identity()
        this_user = User.query.filter(User.email == current_user).first()
        
        if not this_user:
            config.log.error(f"Unable to find a user in the database that is attempting to register a new report. Error: {err}.")
            return jsonify({"error_message": "Unable to create a new user report."}), 400
        
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
            target=target)

        db.session.add(record)
        db.session.commit()

        return jsonify({"report_id": f"{record.report_id}"}), 200

    except Exception as err:
        config.log.error(f"Unable to create a new report. Error: {err}.")
        return jsonify({"error_message": "Unable to register a new report."}), 500