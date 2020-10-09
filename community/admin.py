from django.contrib.admin import site

from .models import Organization

site.register(Organization)
