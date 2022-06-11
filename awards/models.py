from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    """
    This class takes care of the posted projects
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    image = CloudinaryField('image')
    title = models.CharField(max_length=50)
    description=models.CharField(max_length=100)
    url = models.TextField()
    posted_date = models.DateTimeField(auto_now_add=True)
    rate = models.IntegerField(default=0)
