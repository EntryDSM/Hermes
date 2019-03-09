from sanic import Blueprint

from user.view import User, Status

bp = Blueprint("user")

bp.add_route(User.as_view(), "/user")
bp.add_route(Status.as_view(), "/user/status")
