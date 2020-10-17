from django.contrib.admin import site, register, ModelAdmin, StackedInline

from .models import Organization, Career, NLHEStat

site.register(Organization)


class NLHEStatInline(StackedInline):
    model = NLHEStat


@register(Career)
class NLHEStatAdmin(ModelAdmin):
    inlines = [NLHEStatInline]
