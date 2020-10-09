from django.views.generic import DetailView
from django_tables2 import SingleTableView

from .models import Room
from .tables import RoomTable


class RoomListView(SingleTableView):
    model = Room
    table_class = RoomTable

    def get_queryset(self):
        return Room.objects.select_subclasses()


class RoomDetailView(DetailView):
    model = Room

    def get_template_names(self):
        return self.get_object().template_path

    def get_object(self, queryset=None):
        return Room.objects.get_subclass(pk=self.kwargs["pk"])
