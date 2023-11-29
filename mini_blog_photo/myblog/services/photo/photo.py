from django.db.models import Count, Q
from service_objects.fields import ModelField
from service_objects.services import Service

from myblog.models import Photo, User, Like, Comment
from django import forms


class PhotoIndexService(Service):

    def process(self):
        return Photo.objects.order_by('-id')


class PhotoSearchService(Service):
    name_photo = forms.CharField()

    def process(self):
        name_photo = self.cleaned_data['name_photo']
        return Photo.objects.filter(title__contains=name_photo).order_by('-id')


class PhotoDetailService(Service):
    id = forms.IntegerField()
    user_id = forms.IntegerField()

    def process(self):
        id = self.cleaned_data['id']
        user_id = self.cleaned_data['user_id']

        photo = Photo.objects.annotate(
            like=Count('likes', filter=Q(likes__is_like=True), distinct=True),
            dislike=Count('likes', filter=Q(likes__is_like=False), distinct=True),
        ).filter(id=id).first()
        comments = photo.comments.all().order_by('-id')
        data = {
            'photo': photo,
            'comments': comments,
        }
        if user_id:
            data['my_like'] = len(Like.objects.filter(photo=photo, user=user_id, is_like=True))
            data['my_dislike'] = len(Like.objects.filter(photo=photo, user=user_id, is_like=False))

        return data


class PhotoNewCommentService(Service):
    id_photo = forms.IntegerField()
    id_user = forms.IntegerField()
    text = forms.CharField()

    def process(self):
        id_photo = self.cleaned_data['id_photo']
        id_user = self.cleaned_data['id_user']
        text = self.cleaned_data['text']
        photo = Photo.objects.get(id=id_photo)
        user = User.objects.get(id=id_user)
        if text != '1':
            Comment.objects.create(text=text, photo=photo, user=user)

        return 1


class PhotoCreateService(Service):
    title = forms.CharField()
    description = forms.CharField()
    user = ModelField(User)
    img = forms.ImageField()

    def process(self):
        title = self.cleaned_data['title']
        description = self.cleaned_data['description']
        user = self.cleaned_data['user']
        img = self.cleaned_data['img']
        Photo.objects.create(title=title, description=description, author=user, img=img)
        return 1


class PhotoEditingService(Service):
    id_photo = forms.IntegerField()
    user = ModelField(User)

    def process(self):
        data = {}
        id_photo = self.cleaned_data['id_photo']
        data['photo'] = Photo.objects.get(id=id_photo)
        user = self.cleaned_data['user']
        data['all_comments'] = user.comments.filter(photo=data['photo'])
        return data


class PhotoDeleteService(Service):
    id_photo = forms.IntegerField()

    def process(self):
        id_hpoto = self.cleaned_data['id_photo']
        Photo.objects.get(id=id_hpoto).delete()
        return 1


class DescriptionEditingService(Service):
    id_photo = forms.IntegerField()
    new_text = forms.CharField()
    new_description = forms.CharField()

    def process(self):
        id_photo = self.cleaned_data['id_photo']
        new_text = self.cleaned_data['new_text']
        new_description = self.cleaned_data['new_description']
        obg = Photo.objects.get(id=id_photo)
        if new_text != '1':
            obg.title = new_text
            obg.save()
        if new_description != '1':
            obg.description = new_description
            obg.save()

        return 1
