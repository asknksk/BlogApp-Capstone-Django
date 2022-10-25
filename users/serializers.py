# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.serializers import TokenSerializer
from .models import Profile


class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all(), # unique email
            message='This Email has been used.')] 
            )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], 
        style={"input_type": "password"} 
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs): # validating if password and password2 match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data): 
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        
        user.set_password(validated_data['password']) 
        user.save()

        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            "id"
        )


class CustomTokenSerializer(TokenSerializer):
    user = UserSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = (
            'key',
            'user'
        )

class ProfileUpdateForm(serializers.ModelSerializer): 
    user = UserSerializer()
    class Meta:
        model = Profile 
        fields = (
            'image',
            'user'
        )

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        instance.image = validated_data.get('image', instance.image)
        instance.save()

        user.username = user_data.get(
            'username',
            user.username
        )
        user.email = user_data.get(
            'email',
            user.email
         )
        user.save()

        return instance