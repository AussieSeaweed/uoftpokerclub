from django.contrib.admin import ModelAdmin
from django.contrib.admin import register

from .models import Category, Post, Event, Correspondence


@register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ["name", "parent"]


@register(Post)
class PostAdmin(ModelAdmin):
    list_display = ["name", "parent", "draft", "important", "created_on", "updated_on"]


@register(Event)
class EventAdmin(ModelAdmin):
    list_display = ["name", "start_time", "end_time"]


@register(Correspondence)
class CorrespondenceAdmin(ModelAdmin):
    list_display = ["subject", "name", "email", "created_on"]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
