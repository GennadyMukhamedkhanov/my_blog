from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PhotoListSerializer, CommentListSerializer, LikeDislikeSerialiser
from myblog.models import Photo, User, Comment, Like

# Todo DefaultRouter не поонял чем он отличается от SimpleRouter
#  Также как работает @action
#  Переопределение метода get_queryset
#  Переопределение routers
# class PhotoViewSet(viewsets.ModelViewSet):
#     queryset = Photo.objects.all()
#     serializer_class = PhotoListSerializer


# class PhotoListView(generics.ListCreateAPIView):
#     queryset = Photo.objects.all()
#     serializer_class = PhotoListSerializer


class PhotoListCreateView(APIView):
    def get(self, request):
        obj_photo = Photo.objects.all()
        obj_sr = PhotoListSerializer(obj_photo, many=True).data
        return Response(obj_sr)

    def post(self, request):
        serializer = PhotoListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
