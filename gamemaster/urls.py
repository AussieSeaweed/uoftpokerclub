from django.urls import path

from gamemaster.views import RoomDetailView, RoomListView

urlpatterns = [
    path('', RoomListView.as_view(), name='room-list'),
    path('<str:pk>/', RoomDetailView.as_view(), name='room-detail'),
]
