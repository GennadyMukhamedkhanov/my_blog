from django.db.models import Count, Q
from service_objects.fields import ModelField
from service_objects.services import Service

from myblog.models import Photo, User, Like, Comment
from django import forms


class CommentsEditingService(Service):
    id_photo = forms.IntegerField()
    id_comment = forms.IntegerField()

    def process(self):
        data = {}
        id_photo = self.cleaned_data['id_photo']
        id_comment = self.cleaned_data['id_comment']
        data['photo'] = Photo.objects.get(id=id_photo)
        data['comment'] = Comment.objects.get(id=id_comment)
        return data


class CommentsNewService(Service):
    new_comment = forms.CharField()
    id_comment = forms.IntegerField()

    def process(self):
        new_comment = self.cleaned_data['new_comment']
        id_comment = self.cleaned_data['id_comment']
        comment = Comment.objects.get(id=id_comment)
        comment.text = new_comment
        comment.save()
        return 1


class CommentDelService(Service):
    id_comment = forms.IntegerField()

    def process(self):
        id_comment = self.cleaned_data['id_comment']
        Comment.objects.get(id=id_comment).delete()
        return 1
