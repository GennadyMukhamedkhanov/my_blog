import io

from rest_framework.parsers import JSONParser

from myblog.models import Photo, Comment, Like, User

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PhotoListSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Photo
        fields = ('__all__')

    # title = serializers.CharField(max_length=100)
    # description = serializers.CharField()
    # create_at = serializers.DateField(read_only=True)
    # status = serializers.BooleanField(default=False)
    # author_id = serializers.IntegerField()
    # img = serializers.ImageField()

    def create(self, validated_data):
        return Photo.objects.create(
            **validated_data

        )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.create_at = validated_data.get('create_at', instance.create_at)
        instance.status = validated_data.get('status', instance.status)
        instance.author_id = validated_data.get('author_id', instance.author_id)
        instance.img = validated_data.get('img', instance.img)
        instance.save()
        return instance


class CommentListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    photo = PhotoListSerializer()

    class Meta:
        model = Comment
        fields = ('__all__')
    # text = serializers.CharField(max_length=250)
    # create_at = serializers.DateField(read_only=True)
    # photo_id = serializers.IntegerField()
    # user_id = serializers.IntegerField()

    def create(self, validated_data):
        return Comment.objects.create(
            **validated_data
        )

        # return Comment.objects.create(
        #     text=validated_data['text'],
        #     photo_id=validated_data['photo_id'],
        #     user_id=validated_data['user_id']
        #
        # )

    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.create_at = validated_data.get('create_at', instance.create_at)
        instance.photo_id = validated_data.get('photo_id', instance.photo_id)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()
        return instance


class LikeDislikeSerialiser(serializers.ModelSerializer):
    photo = PhotoListSerializer()
    user = UserSerializer()

    class Meta:
        model = Like
        fields = ('__all__')
    # photo_id = serializers.IntegerField()
    # user_id = serializers.IntegerField()
    # is_like = serializers.BooleanField(default=True)

    def create(self, validated_data):
        return Like.objects.create(
            **validated_data
        )

    def update(self, instance, validated_data):
        instance.photo_id = validated_data.get('photo_id', instance.photo_id)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.is_like = validated_data.get('is_like', instance.is_like)
        instance.save()
        return instance


class ListSerializer(serializers.ModelSerializer):
    pass
