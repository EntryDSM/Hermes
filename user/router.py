from sanic import Blueprint

from user.view import (UserView, UserInfoView, UserStatusView, UserBatchView, AdminView, AdminInfoView, AdminBatchView)

bp = Blueprint("user", url_prefix="/api/v1")

bp.add_route(UserView.as_view(), "/user")
bp.add_route(UserInfoView.as_view(), "/user/<user_email>")
bp.add_route(UserBatchView.as_view(), "/user/batch")
bp.add_route(UserStatusView.as_view(), "/user/status")
bp.add_route(AdminView.as_view(), "/admin")
bp.add_route(AdminInfoView.as_view(), "/admin/<admin_id>")
bp.add_route(AdminBatchView.as_view(), "/admin/batch")
