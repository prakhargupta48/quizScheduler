from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_file, name='upload_file'),
    path('download_schedule/', views.download_schedule, name='download_schedule'),
]
