from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from .models import Profile, Career


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ["url", "gravatar_url"]


class CareerSerializer(ModelSerializer):
    class Meta:
        model = Career
        fields = []


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()
    career = CareerSerializer()

    class Meta:
        model = get_user_model()
        fields = ["username", "profile", "career"]
