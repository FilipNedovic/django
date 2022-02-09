from django.urls import path
from todos import views

urlpatterns = [
    path('', views.HomeView.home),
    path('users/', views.UserViewSet.as_view(), name='users'),
    path('users/<int:pk>/', views.UserViewDetail.as_view(), name='user'),
    path('users/create/', views.CreateUserAPIView.as_view(), name='create'),
    path('users/me/', views.UserRetrieveUpdateAPIView.as_view(), name='me'),
    path('users/filter', views.FilterUsersAPIView.as_view(), name='filter'),
    path('todos/', views.TodoViewSet.as_view(), name='todos'),
    path('todos/<int:pk>/', views.TodoViewDetail.as_view(), name='todo'),
]