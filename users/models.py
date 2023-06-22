from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    phone_number=models.BigIntegerField()
    user=models.OneToOneField(User,related_name="profile",on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name
    
class OTP(models.Model):
    email=models.EmailField()
    otp_number=models.IntegerField()

    def __str__(self):
        return f"{self.email}-{self.otp_number}"