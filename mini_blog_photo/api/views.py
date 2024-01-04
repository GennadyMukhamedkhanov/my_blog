from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from api.permissions.photo.permissions import OnlyReadOrIsAdminUser
from api.serializers import PhotoListSerializer, CommentListSerializer, LikeDislikeSerialiser, \
    PersonalAccountSerializer, UserCreateTokenSerializer, UpdatePhohoUserSerializer, ListCommentsLikePhotoSerializer, \
    UserCreateSerializer, CreatePhotoSerializer, CoommentsPersonalOnPhotoAllSerializer, CoommentsSerializer, \
    AllDataSerializer
from myblog.models import Photo, User, Comment, Like


class UserCreateView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            phone=serializer.validated_data['phone']
        )
        token = Token.objects.create(user=user)
        return Response(UserCreateTokenSerializer(user).data)


class TokenGetView(APIView):
    def post(self, request):
        user = User.objects.filter(
            username=request.data['username']
        )
        if not user.exists():
            return Response({
                'error': 'Data is not valid'
            }, status=404)
        if user.first().check_password(request.data['password']):
            return Response({
                'token': (user.first().auth_token).key
            })
        return Response({
            'error': 'Data is not valid'
        }, status=400)

class PhotoListCreateView(APIView):
    def get(self, request):
        permission_classes = [AllowAny, ]
        self.check_permissions(request)
        obj_photo = Photo.objects.all()
        obj_sr = PhotoListSerializer(obj_photo, many=True).data
        return Response(obj_sr)

    def post(self, request, **kwargs):
        permission_classes = [IsAuthenticated, ]
        self.check_permissions(request)
        serializer = CreatePhotoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Photo.objects.create(
            title=serializer.validated_data['title'],
            description=serializer.validated_data['description'],
            author=request.user,
            img=serializer.validated_data['img']
        )
        obj_ser = UpdatePhohoUserSerializer(instance).data
        return Response({'New photo': obj_ser})


class PhotoShowUpdateDeleteView(APIView):
    def put(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated, IsAdminUser]

        id_photo = kwargs.get('pk_photo')
        try:
            instance = Photo.objects.get(pk=id_photo)
        except:
            return Response({'error': 'Фото с данны id не существует'})
        # Todo так нужно?
        if request.user.id != instance.author_id:
            return Response({
                'error': 'You can only change your photos'
            })
        serializer = UpdatePhohoUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.title = serializer.validated_data['title']
        instance.description = serializer.validated_data['description']
        instance.save()
        obj_ser = UpdatePhohoUserSerializer(instance).data
        return Response({'Изменено на': obj_ser})

    def delete(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated, IsAdminUser]
        id_photo = kwargs.get('pk_photo')
        try:
            obj = Photo.objects.get(pk=id_photo)
            # Todo так нужно?
            if request.user.id != obj.author_id:
                return Response({
                    'error': 'You can only delete your photos'
                })
            obj.delete()
        except:
            return Response({'error': 'Ошибка удаления фото'})

        return Response({'Удаление фото': 'прошло успешно'})


class PersonalAccount(APIView):
    def get(self, request, *args, **kwargs):
        permission_classes = [IsAuthenticated, ]
        obj_sr = PersonalAccountSerializer(request.user)
        return Response(obj_sr.data)


class PersonalCommentsUserListUpdateDeleteOnPhoto(APIView):
    def get(self, request, **kwargs):
        # Todo не пойму как данныу о фото передать
        permission_classes = [IsAuthenticatedOrReadOnly]
        id_photo = kwargs.get('pk_photo')
        try:
            photo = Photo.objects.get(id=id_photo)
        except:
            return Response({
                'error':'No photo found'
            })
        if request.user.id != photo.author_id:
            return Response({
                'error': 'You can only delete your photos'
            })

        serializer = CoommentsSerializer(photo).data
        return Response({
            'data_on_photo': serializer,

        })

    def put(self, request, **kwargs):
        permission_classes = [IsAuthenticated, ]
        id_comments = kwargs.get('pk_comments')
        try:
            instance = Comment.objects.get(pk=id_comments)
        except:
            return Response({'error': 'Комментарий с данны id не существует'})
        # Todo так нужно?
        if request.user.id != instance.user_id:
            return Response({
                'error': 'You can only change comments your photos'
            })
        serializer = CoommentsPersonalOnPhotoAllSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.text = serializer.validated_data['text']
        instance.save()
        obj_ser = CoommentsPersonalOnPhotoAllSerializer(instance).data
        return Response({'Изменено на': obj_ser})

    def delete(self, request, **kwargs):
        permission_classes = [IsAuthenticated, ]
        id_comments = kwargs.get('pk_comments')
        try:
            instance = Comment.objects.get(pk=id_comments)
        except:
            return Response({'error': 'Комментарий с данны id не существует'})
        # Todo так нужно?
        if request.user.id != instance.user_id:
            return Response({
                'error': 'You can only delete your comments'
            })

        instance.delete()

        return Response({'Удаление комментария': 'прошло успешно'})


class CommentsListCreateUpdateDeleteView(APIView):
    def get(self, request, **kwargs):
        permission_classes = [IsAuthenticatedOrReadOnly]
        id_photo = kwargs['photo_pk']
        try:
            obj_photo = Photo.objects.get(pk=id_photo)
        except:
            return Response({
                'error':'No photo found'
            })
        obj_ser = ListCommentsLikePhotoSerializer(obj_photo).data
        return Response(obj_ser)

    def post(self, request, **kwargs):
        id_photo = kwargs['photo_pk']
        serializer = CoommentsPersonalOnPhotoAllSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            obj_photo = Comment.objects.create(
            text=serializer.validated_data['text'],
            photo_id=id_photo,
            user=request.user,
        )
        except:
            return Response({
                'error': 'No photo found'
            })
        obj_ser = CommentListSerializer(obj_photo).data
        return Response({'New comments': obj_ser})

# Todo------------------------------------------------------------------
class AllData(APIView):
    def get(self, request):
        photos = Photo.objects.all()
        serializer = AllDataSerializer(photos, many=True)
        return Response({
            'data':serializer.data
        })



# class PhotoPutDelete(APIView):
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         try:
#             instance = Photo.objects.get(pk=pk)
#         except:
#             return Response({'error': f'Объект c id:{pk} не определен '})
#
#         serializer = PhotoListSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         try:
#             Photo.objects.get(pk=pk).delete()
#         except:
#             return Response({'error': f'Объект с id {pk} не существует'})
#         return Response({'STATUS': 'Объект удален'})
#
#
# class CommentListCreateView(APIView):
#     def get(self, request):
#         obj_photo = Comment.objects.all()
#         obj_sr = CommentListSerializer(obj_photo, many=True).data
#         return Response(obj_sr)
#
#     def post(self, request):
#         serializer = CommentListSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data)
#
#
# class CommentPutDelete(APIView):
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         try:
#             instance = Comment.objects.get(pk=pk)
#         except:
#             return Response({'error': f'Объект с id {pk} не существует'})
#
#         serializer = CommentListSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#
#         try:
#             instance = Comment.objects.get(pk=pk)
#             instance.delete()
#         except:
#             return Response({'error': 'Объект не определен'})
#
#         return Response({f'comments c pk {pk}': 'удален'})
#
#
# class LikeDislikeCreate(APIView):
#     def get(self, request):
#         list_obj_like = Like.objects.all()
#         list_ser = LikeDislikeSerialiser(list_obj_like, many=True).data
#         return Response(list_ser)
#
#     def post(self, request):
#         serializer = LikeDislikeSerialiser(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#
# class LikeDislikePutDelete(APIView):
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         try:
#             instance = Like.objects.get(pk=pk)
#         except:
#             return Response({'error': f'Объект с id {pk} не существует'})
#         serializer = LikeDislikeSerialiser(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk')
#         try:
#             Like.objects.get(pk=pk).delete()
#         except:
#             return Response({'error': f'Объект с id {pk} не существует'})
#         return Response({'STATUS': 'Объект удален'})
