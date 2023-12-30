from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from api.serializers import PhotoListSerializer, CommentListSerializer, LikeDislikeSerialiser, \
    PersonalAccountSerializer, UserCreateTokenSerializer, UpdatePhohoUserSerializer, ListCommentsLikePhotoSerializer
from myblog.models import Photo, User, Comment, Like


class UserCreateView(APIView):
    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')
        phone = request.data.get('phone')
        user = User.objects.create_user(username=login, password=password, phone=phone)
        token = Token.objects.create(user=user)
        #tk = token.pk
        return Response(UserCreateTokenSerializer(user).data)


class PhotoListCreateView(APIView):
    #permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request):
        #tok = request.user

        #permission_classes = (IsAdminUser,)

        obj_photo = Photo.objects.all()
        obj_sr = PhotoListSerializer(obj_photo, many=True).data
        return Response(obj_sr)



class PersonalAccount(APIView):
    def get(self, request, *args, **kwargs):
        pk_user = kwargs.get('pk')
        obj_user = User.objects.get(pk=pk_user)
        obj_sr = PersonalAccountSerializer(obj_user)
        return Response(obj_sr.data)


class CreateUpdateDeletePhohoUser(APIView):
    # Todo правильно ли передавать данные пользователя через динамическую ссылку
    #  или нужно каким то другим способом (request.user, показывает что аноним),
    #  и в целом правильно ли применен сериализатор
    def post(self, request, **kwargs):
        id_user = kwargs.get('user_pk')
        try:
            obj_user = User.objects.get(pk=id_user)
        except:
            return Response({'error': 'Пользователя с таким id нет'})

        serializer = UpdatePhohoUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

#____________________________________________________________________________
        title = serializer.validated_data['title']
        description = serializer.validated_data['description']
        author = obj_user
        img = serializer.validated_data['img']

        instance = Photo.objects.create(
            title=title,
            description=description,
            author=author,
            img=img
        )
        obj_ser = UpdatePhohoUserSerializer(instance).data
#_____________________________________________________________________________
        return Response({'New photo': obj_ser})
    def put(self, request, *args, **kwargs):
        id_photo = kwargs.get('pk')
        try:
            instance = Photo.objects.get(pk=id_photo)
        except:
            return Response({'error': 'Фото с данны id не существует'})

        instance.title = request.data['title']
        instance.description = request.data['description']
        instance.save()
        obj_ser = UpdatePhohoUserSerializer(instance).data
        return Response({'Изменено на': obj_ser})

    def delete(self, request, *args, **kwargs):
        id_photo = kwargs.get('pk')
        try:
            Photo.objects.get(pk=id_photo).delete()
        except:
            return Response({'error': 'Ошибка удаления фото'})

        return Response({'Удаление фото': 'прошло успешно'})



class ListCommentsLikePhoto(APIView):
    def get(self, request, **kwargs):
        id_photo = kwargs['photo_pk']
        obj_photo = Photo.objects.get(pk=id_photo)
        obj_ser = ListCommentsLikePhotoSerializer(obj_photo).data
        return Response(obj_ser)



# Todo или так пользователя передавать?
    def post(self, request, **kwargs):
        id_photo = kwargs['photo_pk']
        obj_photo = Comment.objects.create(
            text=request.data['text'],
            photo_id=id_photo,
            user_id=request.data['user'],
        )
        obj_ser = CommentListSerializer(obj_photo).data
        return Response({'New comments':obj_ser})


















# Todo------------------------------------------------------------------

class PhotoPutDelete(APIView):
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        try:
            instance = Photo.objects.get(pk=pk)
        except:
            return Response({'error': f'Объект c id:{pk} не определен '})

        serializer = PhotoListSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            Photo.objects.get(pk=pk).delete()
        except:
            return Response({'error': f'Объект с id {pk} не существует'})
        return Response({'STATUS': 'Объект удален'})


class CommentListCreateView(APIView):
    def get(self, request):
        obj_photo = Comment.objects.all()
        obj_sr = CommentListSerializer(obj_photo, many=True).data
        return Response(obj_sr)

    def post(self, request):
        serializer = CommentListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class CommentPutDelete(APIView):
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        try:
            instance = Comment.objects.get(pk=pk)
        except:
            return Response({'error': f'Объект с id {pk} не существует'})

        serializer = CommentListSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)

        try:
            instance = Comment.objects.get(pk=pk)
            instance.delete()
        except:
            return Response({'error': 'Объект не определен'})

        return Response({f'comments c pk {pk}': 'удален'})


class LikeDislikeCreate(APIView):
    def get(self, request):
        list_obj_like = Like.objects.all()
        list_ser = LikeDislikeSerialiser(list_obj_like, many=True).data
        return Response(list_ser)

    def post(self, request):
        serializer = LikeDislikeSerialiser(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LikeDislikePutDelete(APIView):
    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        try:
            instance = Like.objects.get(pk=pk)
        except:
            return Response({'error': f'Объект с id {pk} не существует'})
        serializer = LikeDislikeSerialiser(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            Like.objects.get(pk=pk).delete()
        except:
            return Response({'error': f'Объект с id {pk} не существует'})
        return Response({'STATUS': 'Объект удален'})
