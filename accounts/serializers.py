from rest_framework import serializers

from accounts.models import User, Tag, UserTag


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    tags = serializers.StringRelatedField(read_only=True, many=True)

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            birth=validated_data['birth'],
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
        fields = ['email', 'password', 'birth', 'gender', 'nickname', 'emoji', 'type', 'tags']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class CreateUserTagSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='email')
    tag = serializers.ListField()

    def create(self, validated_data):
        user = User.objects.get(email=validated_data['user'])
        user_tags = []
        for tag_id in validated_data['tag']:
            user_tags.append(UserTag(user=user, tag_id=tag_id))
        return UserTag.objects.bulk_create(user_tags)

    class Meta:
        model = UserTag
        fields = ['user', 'tag']
