from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # user_type = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField("password", max_length=128)
    weigth = models.CharField(max_length=5)
    heigth = models.CharField(max_length=5)
    birthdate = models.CharField(max_length=15)
    def __str__(self):
        return "Όνομα: " + str(self.name) + " Επώνυμο:" + self.last_name + "email: " + self.email+ "weigth: " + self.weigth+ "heigth: " + self.heigth



class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
