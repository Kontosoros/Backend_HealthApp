from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.CharField(max_length=200)
    password = models.CharField("password", max_length=128)
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
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

class Diagnostic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    age = models.SmallIntegerField(null=True)
    pregnancies  = models.SmallIntegerField(null=True)
    glucose = models.SmallIntegerField(null=True)
    bloodpressure = models.SmallIntegerField(null=True)
    skinthickness  = models.SmallIntegerField(null=True)
    insulin = models.SmallIntegerField(null=True)
    bmi = models.SmallIntegerField(null=True)
    diabetespedigree = models.SmallIntegerField(null=True)
    sex = models.CharField(max_length=255)
    trtbps = models.SmallIntegerField(null=True)
    chol = models.SmallIntegerField(null=True)
    fbs = models.SmallIntegerField(null=True)
    thalachh = models.SmallIntegerField(null=True)
    exng = models.SmallIntegerField(null=True)
    thall = models.SmallIntegerField(null=True)


