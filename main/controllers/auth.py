from flask import jsonify

from main import app
from main.commons.decorators import validate_request
from main.commons.exceptions import BadRequest
from main.engines import user as user_engine
from main.libs.jwt import create_access_token
from main.schemas.auth import AuthSchema


@app.route("/auth", methods=["POST"])
@validate_request("body", AuthSchema)
def login(data):
    user = user_engine.find_by_email_and_password(**data)
    if user is None:
        raise BadRequest()
    return jsonify(access_token=create_access_token(user.id))
