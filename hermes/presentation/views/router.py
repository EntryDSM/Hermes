from sanic import Blueprint

from hermes.presentation.views.admin import AdminBatchView, AdminDetailView, AdminView

# from hermes_v2.presentation.views.applicant import (UserView, UserInfoView,
#                                                     UserStatusView, UserBatchView)

bp = Blueprint("user", url_prefix="/api/v1")  # pylint: disable=invalid-name

# bp.add_route(UserView.as_view(), "/user")
# bp.add_route(UserInfoView.as_view(), "/user/<user_email>")
# bp.add_route(UserBatchView.as_view(), "/user/batch")
# bp.add_route(UserStatusView.as_view(), "/user/status")
bp.add_route(AdminView.as_view(), "/admin")
bp.add_route(AdminDetailView.as_view(), "/admin/<admin_id>")
bp.add_route(AdminBatchView.as_view(), "/admin/batch")
