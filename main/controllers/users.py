from flask import jsonify

from main import app
from main.commons.decorators import require_authorized_user, validate_request
from main.commons.exceptions import BadRequest
from main.engines import user as user_engine
from main.libs.jwt import create_access_token
from main.schemas.user import UserSchema


@app.route("/users", methods=["POST"])
@validate_request("body", UserSchema)
def register(data):
    if user_engine.find_by_email(data["email"]):
        raise BadRequest(error_message=f"{data['email']} already existed")
    user = user_engine.create_user(**data)
    return jsonify(access_token=create_access_token(user.id))


@app.route("/users/me", methods=["GET"])
@require_authorized_user
def get_profile(user):
    return UserSchema().jsonify(user)
