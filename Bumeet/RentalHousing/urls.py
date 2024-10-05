from django.urls import path
from .views import *

urlpatterns = [
    path('rental_api/<int:pageNo>/<int:rows>/', ResponseRentalHousingView.as_view(), name='rental_housing'),
]