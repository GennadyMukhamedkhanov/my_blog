from service_objects.services import Service

from myblog.models import Photo, User, Like
from django import forms


class LikeService(Service):
    id_photo = forms.IntegerField()
    id_user = forms.IntegerField()

    def process(self):
        id_photo = self.cleaned_data['id_photo']
        id_user = self.cleaned_data['id_user']
        user_obj = User.objects.get(id=id_user)
        photo = Photo.objects.get(id=id_photo)
        try:
            like = Like.objects.get(photo=photo, user=user_obj)
            if like.is_like == False:
                Like.objects.filter(photo=photo, user=user_obj).update(is_like=True)

        except:
            Like.objects.create(photo=photo, user=user_obj, is_like=True)
        return self

class DislikeService(Service):
    user_id = forms.IntegerField()
    photo_id = forms.IntegerField()


    def process(self):
        user_id = self.cleaned_data['user_id']
        photo_id = self.cleaned_data['photo_id']
        photo_obj = Photo.objects.get(id=photo_id)
        user_obj = User.objects.get(id=user_id)
        try:
            dislike = Like.objects.get(photo=photo_obj, user=user_obj)
            if dislike.is_like == True:
                Like.objects.filter(photo=photo_obj, user=user_obj).update(is_like=False)

        except:
            Like.objects.create(photo=photo_obj, user=user_obj, is_like=False)

        return self
