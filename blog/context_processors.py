from datetime import datetime

from django.conf import settings

from .models import Post, Event


def blog(request):
    cur_time = datetime.now()

    return {
        "recent_posts": Post.objects.filter(draft=False).order_by("-created_on")[:settings.NUM_RECENT_POSTS],
        "ongoing_events": Event.objects.filter(start_time__lte=cur_time).filter(end_time__gt=cur_time),
        "scheduled_events": Event.objects.filter(start_time__gt=cur_time),
    }
