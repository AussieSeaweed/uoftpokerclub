from django.views.generic import ListView, DetailView

from gamemaster.models import Room


class RoomListView(ListView):
    model = Room

    def get_queryset(self):
        return Room.objects.select_subclasses()


class RoomDetailView(DetailView):
    model = Room
    template_name = 'gamemaster/room_detail.html'

    def get_object(self, queryset=None):
        return Room.objects.get_subclass(pk=self.kwargs['pk'])
