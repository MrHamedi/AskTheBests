from rest_framework import serializers

from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction


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
            request=self.context.get('request'),
            email=attrs['email'],
            password=attrs['password']
        )
        if (user == None):
            raise serializers.ValidationError(
                "The provided email or password is incorrect!"
            )
        attrs['user'] = user
        return attrs


class UserInfoUpdateSerializer(serializers.ModelSerializer):
    profile_image=serializers.ImageField(allow_empty_file=True,
                                         source='profile.pic',
                                         label="عکس پروفایل",
                                        )
    
    class Meta:
        model=get_user_model()
        fields=('email', 'date_of_birth', 'profile_image')

    def update(self, instance, validated_data):
        with transaction.atomic():
            instance.email=validated_data.get("email", instance.email)
            instance.date_of_birth=validated_data.get("date_of_birth",
                                                       instance.date_of_birth)
            instance.save()
            profile_image = validated_data.get("profile").get("pic")
            if profile_image:
                instance.profile.pic = profile_image
                instance.profile.save()
        return instance