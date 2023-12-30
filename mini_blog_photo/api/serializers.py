import io

from rest_framework.parsers import JSONParser

from myblog.models import Photo, Comment, Like, User

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

class UserCreateTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone',)

# Vasia 333
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class PhotoListSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Photo
        fields = ('title', 'img', 'author', 'create_at')


# Todo -----------------------------------------------------

class PhotoImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('img',)


class PersonalAccountSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    comments_my_count = serializers.SerializerMethodField()
    photo_my = serializers.SerializerMethodField()
    sum_like_dislike = serializers.SerializerMethodField()

    def get_sum_like_dislike(self, obj):
        return obj.likes.all().count()
    def get_likes_count(self, obj):
        like = obj.likes.filter(is_like=True).count()
        return like

    def get_dislikes_count(self, obj):
        dislike = obj.likes.filter(is_like=False).count()
        return dislike

    def get_comments_my_count(self, obj):
        comments = obj.comments.all().count()
        return comments

    def get_photo_my(self, obj):
        photos = obj.photos.all()
        return PhotoImgSerializer(photos, many=True).data

    class Meta:
        model = User
        fields = (
            'username',
            'phone',
            'email',
            'likes_count',
            'dislikes_count',
            'comments_my_count',
            'photo_my',
            'sum_like_dislike',
        )


# Todo -----------------------------------------------------

class UpdatePhohoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('__all__')




class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('text',)

class CommentUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class ListCommentsLikePhotoSerializer(serializers.ModelSerializer):
    author = CommentUserSerializers()
    comments = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    dislike = serializers.SerializerMethodField()

    def get_dislike(self, obj):
        return obj.likes.filter(is_like=False).count()
    def get_like(self, obj):
        return obj.likes.filter(is_like=True).count()

    def get_comments(self, obj):
        all_comments = obj.comments.all()
        return CommentsSerializer(all_comments, many=True).data


    class Meta:
        model = Photo
        fields = ('title',
                  'author',
                  'create_at',
                  'description',
                  'comments',
                  'like',
                  'dislike')
        #like, photo




















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
