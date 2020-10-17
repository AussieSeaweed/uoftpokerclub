from django.contrib.admin import site

from .models import Organization, Career

site.register(Organization)
site.register(Career)
