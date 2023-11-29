from django import forms
from django.contrib.auth import authenticate
from django.db.models import Count, Q, F
from service_objects.fields import DictField
from service_objects.services import Service

from myblog.models import User, Photo


class UserRegistrationService(Service):
    username = forms.CharField()
    password = forms.CharField()
    phone = forms.CharField()

    def process(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        phone = self.cleaned_data['phone']
        User.objects.create_user(username=username, password=password, phone=phone)
        return 1


class UserAuthorizationService(Service):
    username = forms.CharField()
    password = forms.CharField()
    request = DictField()

    def process(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        request = self.cleaned_data['request']
        user = authenticate(request, username=username, password=password)
        return user


class UserPersonalAccountService(Service):
    user_id = forms.IntegerField()

    def process(self):
        data = {}
        user_id = self.cleaned_data['user_id']
        data['user'] = User.objects.annotate(
            likes_count=Count('likes', filter=Q(likes__is_like=True), distinct=True),
            dislikes_count=Count('likes', filter=Q(likes__is_like=False), distinct=True),
            sum_likes=F('likes_count') + F('dislikes_count'),
            comments_count=Count('comments', distinct=True)
        ).filter(id=user_id).first()
        author = User.objects.get(id=user_id)
        data['my_photo'] = Photo.objects.filter(author=author)
        return data
