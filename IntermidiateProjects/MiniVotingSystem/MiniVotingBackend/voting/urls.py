from django.urls import path
from .views import CandidatesAPIView, ElectionsAPIView, RegisterUsersAPIView, LoginApIView, UserSearchAPIView, VotesAPIView

urlpatterns = [
    path('register/', RegisterUsersAPIView.as_view(), name='register'),
    path('login/', LoginApIView.as_view(), name='login'),
    path('users/', UserSearchAPIView.as_view(), name='user-search'),
    path('votes/', VotesAPIView.as_view(), name='votes'),
    path('addVote/<int:candidate_id>/', VotesAPIView.as_view(), name='add-vote'),
    path('elections/', ElectionsAPIView.as_view(), name='elections'),
    path('candidates/', CandidatesAPIView.as_view(), name='candidates'),
]