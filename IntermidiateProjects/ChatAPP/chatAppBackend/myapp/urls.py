from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('register/', views.RegisterUsersAPIView.as_view(), name='register'),
    path('login/', views.LoginApIView.as_view(), name='login'),
    path('api/chat/', views.ChatMessageListCreateView.as_view(), name='chat-message-list-create'),
    path('users/', views.UserSearchAPIView.as_view(), name='user-search'),
]
