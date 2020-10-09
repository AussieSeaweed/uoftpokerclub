from django.urls import path

from .views import UserListView, UserCreateView, UserUpdateView, UserDetailView, \
    OrganizationListView, OrganizationDetailView

urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("users/update/", UserUpdateView.as_view(), name="user-update"),

    path("organizations/", OrganizationListView.as_view(), name="organization-list"),
    path("organizations/<int:pk>/", OrganizationDetailView.as_view(), name="organization-detail"),
]
