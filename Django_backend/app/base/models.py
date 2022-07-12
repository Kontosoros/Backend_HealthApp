from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    # user_type = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField("password", max_length=128)
    # vat_number = models.CharField(max_length=50)
    # photo = models.ImageField(max_length=500)
    def __str__(self):
        return "Όνομα: " + str(self.name) + " Επώνυμο:" + self.last_name + "email: " + self.email


class Pattient(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    Fk_userID = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Όνομα: " + str(self.name) + " Επώνυμο: " + self.last_name + " email: " + self.email + " Τηλέφωνο: " + str(self.phone)


class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
