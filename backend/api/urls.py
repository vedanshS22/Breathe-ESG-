from django.urls import path

from api.views.audit_views import AuditLogListView, DeleteAllIngestionDataView, IngestionIssueListView
from api.views.company_views import CompanyListView
from api.views.dashboard_views import DashboardView
from api.views.record_views import (
    ApproveRecordView,
    ExportNormalizedRecordsView,
    ExportRawRecordsView,
    RecordDetailView,
    RecordListView,
    RejectRecordView,
    SuspiciousRecordListView,
)
from api.views.upload_views import UploadListView


urlpatterns = [
    path("companies/", CompanyListView.as_view(), name="companies"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("uploads/", UploadListView.as_view(), name="uploads"),
    path("records/", RecordListView.as_view(), name="records"),
    path("records/suspicious/", SuspiciousRecordListView.as_view(), name="suspicious-records"),
    path("records/export/raw/", ExportRawRecordsView.as_view(), name="export-raw-records"),
    path("records/export/normalized/", ExportNormalizedRecordsView.as_view(), name="export-normalized-records"),
    path("records/<int:record_id>/", RecordDetailView.as_view(), name="record-detail"),
    path("records/<int:record_id>/approve/", ApproveRecordView.as_view(), name="approve-record"),
    path("records/<int:record_id>/reject/", RejectRecordView.as_view(), name="reject-record"),
    path("audit-logs/", AuditLogListView.as_view(), name="audit-logs"),
    path("ingestion-issues/", IngestionIssueListView.as_view(), name="ingestion-issues"),
    path("delete-all-ingestion-data/", DeleteAllIngestionDataView.as_view(), name="delete-all-ingestion-data"),
]
