from django.urls import path

from .views import RoomListView, RoomDetailView

urlpatterns = [
    path("rooms/", RoomListView.as_view(), name="room-list"),
    path("rooms/<int:pk>/", RoomDetailView.as_view(), name="room-detail"),
]
