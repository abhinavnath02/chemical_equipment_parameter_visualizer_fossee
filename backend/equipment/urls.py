from django.urls import path
from .views import UploadCSVView, HistoryView, GeneratePDFView, DatasetDetailView

urlpatterns = [
    path('upload/', UploadCSVView.as_view()),
    path('history/', HistoryView.as_view()),
    path('generate-pdf/', GeneratePDFView.as_view()),
    path('dataset/<int:dataset_id>/', DatasetDetailView.as_view()),
]
