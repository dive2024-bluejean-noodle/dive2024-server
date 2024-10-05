from django.urls import path
from .views import *

urlpatterns = [
    path('create/',MatchingCreateView.as_view(), name='matching-create'),
    path('list/', MatchingListView.as_view(), name='matching-list'),
    path('match/<int:pk>',  MatchingDetailView.as_view(), name='matching-detail'),
    path('application/<int:pk>', MatchingUpdateView.as_view(), name="matching-apply"),
    path('delete/<int:pk>', MatchingDeleteView.as_view(), name="matching-delete"),
    path('match/<int:matching_id>/comment/', CommentCreateView.as_view(), name='create_comment'),
]
