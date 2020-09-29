from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django_tables2.views import SingleTableView

from .forms import CustomUserCreationForm
from .tables import UserTable


class UserListView(SingleTableView):
    model = get_user_model()
    table_class = UserTable


class UserCreateView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm

    def get_success_url(self):
        login(self.request, self.object)

        return reverse("home")


class UserDetailView(DetailView):
    model = get_user_model()
    context_object_name = "_user"
