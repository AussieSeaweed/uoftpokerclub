from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Profile, Career


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["url", "gravatar_url"]


class CareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = []


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    career = CareerSerializer()

    class Meta:
        model = get_user_model()
        fields = ["username", "profile", "career"]
