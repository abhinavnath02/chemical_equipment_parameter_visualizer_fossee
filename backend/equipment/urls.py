from django.urls import path
from .views import UploadCSVView, HistoryView, GeneratePDFView

urlpatterns = [
    path('upload/', UploadCSVView.as_view()),
    path('history/', HistoryView.as_view()),
    path('generate-pdf/', GeneratePDFView.as_view()),
]
