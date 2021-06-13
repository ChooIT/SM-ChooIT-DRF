from rest_framework import serializers

from accounts.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    nickname = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            gender=validated_data['gender'],
            nickname=validated_data['nickname']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        field = ['email', 'password', 'gender', 'nickname']
