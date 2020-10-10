from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django_tables2.views import SingleTableView, SingleTableMixin
from extra_views import UpdateWithInlinesView, InlineFormSet

from .forms import CustomUserCreationForm
from .models import Profile, Organization
from .tables import UserTable, OrganizationTable


class UserListView(SingleTableView):
    model = get_user_model()
    table_class = UserTable


class UserCreateView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm

    def get_success_url(self):
        login(self.request, self.object)

        return reverse("home")


class ProfileInline(InlineFormSet):
    model = Profile
    fields = ["description"]
    factory_kwargs = {"can_delete": False}

    def get_object(self):
        return self.request.user.profile


class UserUpdateView(LoginRequiredMixin, UpdateWithInlinesView):
    model = get_user_model()
    fields = ["username", "first_name", "last_name", "email"]
    inlines = [ProfileInline]
    template_name = "auth/user_update.html"

    def test_func(self):
        return self.request.user.is_authenticated

    def get_success_url(self):
        return reverse("user-detail", kwargs={"pk": self.object.id})

    def get_object(self, queryset=None):
        return self.request.user


class UserDetailView(SingleTableMixin, DetailView):
    model = get_user_model()
    context_object_name = "_user"

    def get_table(self, **kwargs):
        return OrganizationTable(self.object.organizations.all())


class OrganizationListView(SingleTableView):
    model = Organization
    table_class = OrganizationTable


class OrganizationDetailView(SingleTableMixin, DetailView):
    model = Organization

    def get_table(self, **kwargs):
        return UserTable(self.object.members.all())

    def post(self, request, *args, **kwargs):
        organization = self.get_object()

        if request.user.is_authenticated:
            if request.user in organization.members.all():
                organization.members.remove(request.user)
            else:
                organization.members.add(request.user)

            return HttpResponseRedirect(reverse("organization-detail", kwargs={"pk": self.get_object().pk}))
        else:
            return HttpResponseForbidden()
