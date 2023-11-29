from django.shortcuts import render
from rest_framework import generics

from api.serializers import PhotoListSerializer
from myblog.models import Photo


class PhotoListView(generics.ListAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer