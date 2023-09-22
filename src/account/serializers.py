from rest_framework import serializers

from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model


class UserCreationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[EmailValidator(message="please insert a valid email address !")])
    class Meta:
        fields = ('email', 'password')
        model = get_user_model()
        extra_kwargs = {"password" : {"write_only": True, "min_length": 5}}
    
    def create(self, validated_fields):
        return get_user_model().objects.create(**validated_fields)