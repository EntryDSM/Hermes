from sanic import Blueprint

from hermes.presentation.views.admin import AdminBatchView, AdminDetailView, AdminView
from hermes.presentation.views.applicant import (
    ApplicantBatchView,
    ApplicantDetailView,
    ApplicantView,
)
from hermes.presentation.views.applicant_status import ApplicantStatusView

bp = Blueprint("user", url_prefix="/api/v1")  # pylint: disable=invalid-name

bp.add_route(ApplicantView.as_view(), "/applicant")
bp.add_route(ApplicantBatchView.as_view(), "/applicant/batch")
bp.add_route(ApplicantDetailView.as_view(), "/applicant/<email>")
bp.add_route(ApplicantStatusView.as_view(), "/applicant/<email>/status")
bp.add_route(AdminView.as_view(), "/admin")
bp.add_route(AdminDetailView.as_view(), "/admin/<admin_id>")
bp.add_route(AdminBatchView.as_view(), "/admin/batch")
