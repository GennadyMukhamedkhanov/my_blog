import io

from rest_framework.parsers import JSONParser

from myblog.models import Photo

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

class PhotoListSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField()
    create_at = serializers.DateField(read_only=True)
    status = serializers.BooleanField(default=False)
    author_id = serializers.IntegerField()
    img = serializers.ImageField()


class CommentListSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=250)
    create_at = serializers.DateField(read_only=True)
    photo_id = serializers.IntegerField()
    user_id = serializers.IntegerField()


#
# class Car:
#     def __init__(self, speed, color):
#         self.speed = speed
#         self.color = color
#
#
# class CarSerializer(serializers.Serializer):
#     speed = serializers.IntegerField()
#     color = serializers.CharField(max_length=15)
#
#
# def encode():
#     obg_car = Car(25, 'Green')
#     obj_ser = CarSerializer(obg_car)
#     print(obj_ser.data)
#     json = JSONRenderer().render(obj_ser.data)
#     print(json)
#
# def decode():
#     stream = io.BytesIO(b'{"speed":25,"color":"Green"}')
#     data = JSONParser().parse(stream)
#     print(data)
#     serializer = CarSerializer(data=data)
#     print(serializer)
#     print(serializer.is_valid())
#     print(serializer.validated_data)
#




#
# class PhotoListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Photo
#         fields = '__all__'
