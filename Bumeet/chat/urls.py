from django.urls import path
from .views import *

urlpatterns = [
    path('query/', ProcessQueryView.as_view(), name='process_query'),
]
