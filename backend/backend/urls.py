from django.urls import path, include

urlpatterns = [
    path('api/', include('equipment.urls')),
]
