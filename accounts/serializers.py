from rest_framework import serializers

from accounts.models import User, Tag, UserTag


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            gender=validated_data['gender'],
            nickname=validated_data['nickname'],
            emoji=validated_data['emoji'],
            type=validated_data['type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email', 'password', 'gender', 'nickname', 'emoji', 'type']


class CreateUserTagSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email')
    tag = serializers.SlugRelatedField(queryset=Tag.objects.all(), slug_field='tag_code')

    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(CreateUserTagSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = UserTag
        fields = ['user', 'tag']
