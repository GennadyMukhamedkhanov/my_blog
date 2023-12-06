from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import PhotoListSerializer, CommentListSerializer
from myblog.models import Photo, User, Comment


# class PhotoListView(generics.ListAPIView):
#     queryset = Photo.objects.all()
#     serializer_class = PhotoListSerializer

class PhotoListView(APIView):
    def get(self, request):
        obj_photo = Photo.objects.all()
        obj_sr = PhotoListSerializer(obj_photo, many=True).data
        return Response(obj_sr)

    def post(self, request):
        serializer = PhotoListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        post_new = Photo.objects.create(
            title=request.data['title'],
            description=request.data['description'],
            author_id=request.data['author_id'],
            img=request.data['img']

        )
        obj_ser = PhotoListSerializer(post_new).data
        return Response(obj_ser)


class CommentListCreateView(APIView):
    def get(self, request):
        obj_photo = Comment.objects.all()
        obj_sr = CommentListSerializer(obj_photo, many=True).data
        return Response(obj_sr)

    def post(self, request):
        serializer = CommentListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment_new = Comment.objects.create(
            text=request.data['text'],
            photo_id=request.data['photo_id'],
            user_id=request.data['user_id']

        )
        obj_ser = CommentListSerializer(comment_new).data
        return Response(obj_ser)

# at 4 14min
