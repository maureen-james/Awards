from .models import Profile, Project
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