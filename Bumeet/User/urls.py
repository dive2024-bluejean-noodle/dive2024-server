from django.urls import path
from .views import *

urlpatterns = [
    # User Data
    path('register/', UserCreateView.as_view(), name='user-register'),
    path('update/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('delete/<int:pk>', UserDeleteView.as_view(), name='user-delete'),
    path('detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),

    # Login
    path('login/', LoginView.as_view(), name='user-login'),
]