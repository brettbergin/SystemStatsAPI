#!/usr/bin/env python3

from datetime import datetime, timezone

from flask import jsonify, request
from flask import Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin

from flask_jwt_extended import jwt_required
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt

from api.extensions import db, jwt
from api.models.users import User
from api.models.token_blocklist import TokenBlocklist


BasePrint = Blueprint("base_print", __name__)


# Callback function to check if a JWT exists in the database blocklist
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
    jti = jwt_payload["jti"]
    token = db.session.query(TokenBlocklist.id).filter_by(jti=jti).one_or_none()
    return token is not None


@BasePrint.route("/", methods=["GET"])
def home():
    return jsonify({"msg": "Welcome To SystemStatsAPI"}), 200


@BasePrint.route("/authenticate", methods=["POST"])
@cross_origin()
def login():
    # If there is no JSON request body, issue 400.
    if not request.json:
        return jsonify({"msg": "Bad client request body"}), 400

    # If email and password are not parameters in the request body
    if "email" not in request.json.keys() and "password" not in request.json.keys():
        return jsonify({"msg": "Bad client request form"}), 400

    # Parse email and password from json request body.
    email = request.json["email"]
    password = request.json["password"]

    # check if user exists in db.
    user = User.query.filter_by(email=email).one_or_none()
    if not user:
        return jsonify({"msg": "Bad username or password"}), 401

    # Check if password is valid.
    if not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad username or password"}), 401

    # Successful login
    user.jwt_issue_count += 1
    db.session.add(user)
    db.session.commit()

    additional_claims = {"user_id": user.id, "issued_with": "sysagent_jwt_issuer"}
    access_token = create_access_token(
        identity=user.email, additional_claims=additional_claims, fresh=True
    )
    refresh_token = create_refresh_token(
        identity=user.email, additional_claims=additional_claims
    )

    return jsonify(access_token=access_token, refresh_token=refresh_token)


@BasePrint.route("/register", methods=["POST"])
def register():
    if not request.json:
        return jsonify({"msg": "Bad client request body"}), 400

    if (
        "username" not in request.json.keys()
        and "password" not in request.json.keys()
        and "email" not in request.json.keys()
    ):
        return jsonify({"msg": "Bad client request form"}), 400

    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if not username or not password or not email:
        return jsonify({"msg": "Bad client request"}), 400

    user_exists = (
        User.query.filter_by(username=username).one_or_none() is not None
        or User.query.filter_by(email=email).one_or_none() is not None
    )

    if not user_exists:
        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password),
            jwt_issue_count=0,
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "Successfully registered new user."}), 200

    else:
        return jsonify({"msg": "Unable to register user."}), 400


@BasePrint.route("/revoke", methods=["GET"])
@jwt_required()
def revoke():
    jti = get_jwt()["jti"]
    record = TokenBlocklist(jti=jti, created_at=datetime.now(timezone.utc))
    db.session.add(record)
    db.session.commit()

    return jsonify({"msg": "token revocation successful"}), 200


# We are using the `refresh=True` options in jwt_required to only allow
# refresh tokens to access this route.
@BasePrint.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    user = User.query.filter(User.email == get_jwt_identity()).one_or_none()
    if not user:
        return jsonify({"msg": "Unable to refresh access token."}), 401

    info_claims = {"user_id": user.id, "issued_with": "sysagent_jwt_issuer"}
    access_token = create_access_token(
        identity=identity, additional_claims=info_claims, fresh=False
    )
    refresh_token = create_refresh_token(
        identity=identity, additional_claims=info_claims
    )
    return jsonify(access_token=access_token, refresh_token=refresh_token)
