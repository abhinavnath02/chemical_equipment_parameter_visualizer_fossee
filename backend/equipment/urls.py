from django.urls import path
from .views import UploadCSVView, HistoryView

urlpatterns = [
    path('upload/', UploadCSVView.as_view()),
    path('history/', HistoryView.as_view()),
]
