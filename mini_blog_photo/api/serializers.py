from rest_framework import serializers

from myblog.models import Photo


class PhotoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'
