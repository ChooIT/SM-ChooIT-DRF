from rest_framework import serializers

from accounts.models import User, Tag, UserTag


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            gender=validated_data['gender'],
            nickname=validated_data['nickname'],
            type=validated_data['type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'password', 'gender', 'nickname']


class CreateUserTagSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all())

    class Meta:
        model = UserTag
        fields = ['user', 'tag']
