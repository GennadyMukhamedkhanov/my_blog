
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from api.permissions.photo.permissions import IsAuthor, IsAuthorComment
from api.serializers import (PhotoListSerializer, CommentListSerializer, PersonalAccountSerializer,
                             UserCreateTokenSerializer, UpdatePhohoUserSerializer, ListCommentsLikePhotoSerializer,
                             UserCreateSerializer, CreatePhotoSerializer, CoommentsPersonalOnPhotoAllSerializer,
                             CoommentsSerializer, PhotoIdSerializer, CommentsIdSerializer)
from myblog.models import Photo, User, Comment


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
        self.permission_classes = [AllowAny, ]
        self.check_permissions(request)
        # Todo как черех сериалтзатор вернуть все объекты
        obj_photo = Photo.objects.all()
        obj_sr = PhotoListSerializer(obj_photo, many=True).data
        return Response(obj_sr)

    def post(self, request, **kwargs):
        self.permission_classes = [IsAuthenticated, ]
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
    def get(self, request, **kwargs):
        self.permission_classes = [IsAuthenticatedOrReadOnly]
        self.check_permissions(request)
        serializer = PhotoIdSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        obj_photo = serializer.validated_data['pk_photo']
        obj_ser = ListCommentsLikePhotoSerializer(obj_photo).data
        return Response(obj_ser)

    def put(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAuthor, ]
        self.check_permissions(request)

        serializer = PhotoIdSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        instance = serializer.validated_data['pk_photo']
        self.check_object_permissions(request=request, obj=instance)

        serializer = UpdatePhohoUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.title = serializer.validated_data['title']
        instance.description = serializer.validated_data['description']
        instance.save()
        obj_ser = UpdatePhohoUserSerializer(instance).data
        return Response({'Изменено на': obj_ser})

    def delete(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAuthor]
        self.check_permissions(request)
        serializer = PhotoIdSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        # Todo   не пойму зачем здесь мы проверяем на ограничение доступа объект?
        obj = serializer.validated_data['pk_photo']
        self.check_object_permissions(request=request, obj=obj)
        obj.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class PersonalAccount(APIView):
    def get(self, request, *args, **kwargs):
        self.permission_classes = [IsAuthenticated, ]
        self.check_permissions(request)
        obj_sr = PersonalAccountSerializer(request.user)
        return Response(obj_sr.data)


class PhotoShowPersonalAccount(APIView):
    def get(self, request, **kwargs):
        self.permission_classes = [IsAuthenticatedOrReadOnly, IsAuthor]
        self.check_permissions(request)
        serislizer = PhotoIdSerializer(data=kwargs)
        serislizer.is_valid(raise_exception=True)
        obj_photo = serislizer.validated_data['pk_photo']
        self.check_object_permissions(request=request, obj=obj_photo)
        serializer = CoommentsSerializer(obj_photo).data
        return Response({
            'data_on_photo': serializer,

        })


class CommentsUpdateDeleteView(APIView):
    def put(self, request, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAuthor]
        self.check_permissions(request)
        serializer = CommentsIdSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        instance = serializer.validated_data['pk_comments']
        self.check_object_permissions(request=request, obj=instance)

        serializer = CoommentsPersonalOnPhotoAllSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.text = serializer.validated_data['text']
        instance.save()
        obj_ser = CoommentsPersonalOnPhotoAllSerializer(instance).data
        return Response({'Изменено на': obj_ser})

    def delete(self, request, **kwargs):
        self.permission_classes = [IsAuthenticated, IsAuthorComment]
        self.check_permissions(request)
        serializers = CommentsIdSerializer(data=kwargs)
        serializers.is_valid(raise_exception=True)
        instance = serializers.validated_data['pk_comments']
        self.check_object_permissions(request=request, obj=instance)
        instance.delete()

        return Response({'Удаление комментария': 'прошло успешно'})


class CommentCreateView(APIView):

    def post(self, request, **kwargs):
        self.permission_classes = (IsAuthenticated,)
        self.check_permissions(request)
        photo_serializer = PhotoIdSerializer(data=kwargs)
        photo_serializer.is_valid(raise_exception=True)

        serializer = CoommentsPersonalOnPhotoAllSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj_photo = Comment.objects.create(
            text=serializer.validated_data['text'],
            photo=photo_serializer.validated_data['pk_photo'],
            user=request.user,
        )

        obj_ser = CommentListSerializer(obj_photo).data
        return Response({'New comments': obj_ser})

# Todo------------------------------------------------------------------
# class AllData(APIView):
#     def get(self, request):
#         photos = Photo.objects.all()
#         serializer = AllDataSerializer(photos, many=True)
#         return Response({
#             'data': serializer.data
#         })

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
