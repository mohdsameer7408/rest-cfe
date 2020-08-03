from rest_framework import serializers

from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label='Email Address')
    email2 = serializers.EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'email2', 'password']

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        email = value
        user = User.objects.filter(email=email)
        if user.exists():
            raise ValidationError('This user has already registered')

        return value

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError('Emails must match...')

        return value

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(allow_blank=True, read_only=True)
    username = serializers.CharField(max_length=150)

    class Meta:
        model = User
        fields = ['username', 'password', 'token']

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(username=username)

        if user.exists():
            if not user.first().check_password(password):
                raise ValidationError('Invalid Password')

            data['token'] = 'some random token'
            return data
        else:
            raise ValidationError('Invalid Username')


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']
