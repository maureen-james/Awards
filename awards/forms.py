from django.contrib.auth import get_user_model

from .models import Profile, Project,Rating
from django import forms

User = get_user_model()

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','image','url']
        widgets= {
            'url':forms.Textarea(attrs={'rows':2,})
        }

class DetailsForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']  

class AddProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','image','url']
        widgets= {
            'url':forms.Textarea(attrs={'rows':2,})
        }              

class RatingForm(forms.ModelForm):
  class Meta:
    model = Rating
    fields = ['design', 'userbility', 'content']
    def save(self, commit=True):
        instance = super().save(commit=False)               