from django.urls import path
from .views import *

urlpatterns = [
    path('job/<int:pk>', JobDetailView.as_view(), name='Job-detail'),
    path('joblist/', JobListView.as_view(), name='Job-list'),
]
