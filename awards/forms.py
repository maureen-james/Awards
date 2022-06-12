from .models import Profile, Project,Rating
from django import forms

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','image','url']
        widgets= {
            'url':forms.Textarea(attrs={'rows':2,})
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','profile_photo'] 

class RatingForm(forms.ModelForm):
  class Meta:
    model = Rating
    fields = ['design', 'userbility', 'content']
    def save(self, commit=True):
        instance = super().save(commit=False)               