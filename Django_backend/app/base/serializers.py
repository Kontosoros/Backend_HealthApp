from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import *



class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "last_name", "password", "username","weigth","heigth","birthdate","is_staff"]
        extra_kwargs = {
            "password": {'write_only': True}
        }
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data) # Δημιουργεί τον χρήστη χωρίς το password
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance