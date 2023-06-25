from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    phone_number=models.BigIntegerField()
    user=models.OneToOneField(User,related_name="profile",on_delete=models.CASCADE)
    is_admin=models.BooleanField(default=False)

    def __str__(self):
        return self.first_name
    
