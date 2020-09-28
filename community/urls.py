from django.urls import path

from .views import UserListView, UserCreateView, UserDetailView

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
