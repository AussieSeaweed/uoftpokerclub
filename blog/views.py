from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView, TemplateView, DetailView

from .models import Category, Post, Correspondence


class CategoryDetailView(DetailView):
    model = Category

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def get_context_data(self, **kwargs):
        category = self.get_object()

        return {
            **super().get_context_data(**kwargs),
            "categories": Category.objects.filter(parent__isnull=True) if category is None else \
                category.categories.all(),
            "posts": Post.objects.filter(parent__isnull=True, draft=False) if category is None else \
                category.posts.filter(draft=False),
        }


class PostDetailView(PermissionRequiredMixin, DetailView):
    model = Post

    def has_permission(self):
        return not self.get_object().draft or self.request.user.is_staff


class CorrespondenceCreateView(CreateView):
    model = Correspondence
    fields = ["name", "email", "subject", "content"]

    def get_success_url(self):
        return reverse("correspondence-create-done")


class CorrespondenceCreateDoneView(TemplateView):
    template_name = "blog/correspondence_create_done.html"
