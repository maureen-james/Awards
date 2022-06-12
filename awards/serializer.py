from rest_framework import serializers
from .models import Project,Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_photo', 'bio', 'user')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'image', 'description', 'url', 'posted_date', 'user','rate')        