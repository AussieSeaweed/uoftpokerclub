from django.contrib.admin import register, site
from django.contrib.admin import ModelAdmin

from .models import Category, Post, Correspondence, Event

site.register(Category)
site.register(Post)
site.register(Event)


@register(Correspondence)
class CorrespondenceAdmin(ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
