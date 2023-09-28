from rest_framework import serializers

from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model, authenticate


class UserCreationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[EmailValidator(
            message="please insert a valid email address !"
        )
        ]
    )

    class Meta:
        fields = ('email', 'password')
        model = get_user_model()
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_fields):
        return get_user_model().objects.create(**validated_fields)


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[EmailValidator(
            message="please insert a valid email address !"
        )
        ]
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        min_length=5,
    )

    def validate(self, attrs):
        user = authenticate(
            self.context.get('request'),
            attrs['email'],
            attrs['password']
        )
        if (user == None):
            raise serializers.ValidationError(
                "The provided email or password is incorrect!"
            )
        attrs['user'] = user
        return attrs
