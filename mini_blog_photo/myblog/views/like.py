from django.shortcuts import redirect
from django.views import View

from myblog.services.like.like import LikeService, DislikeService


class LikeView(View):
    def get(self, request, **kwargs):
        LikeService.execute(
            {
                'id_photo': kwargs['id'],
                'id_user': request.user.id,

            }
        )
        return redirect('post', kwargs['id'])


class DislikeView(View):
    def get(self, request, **kwargs):
        DislikeService.execute(
            {
                'user_id': request.user.id,
                'photo_id': kwargs['id'],

            }
        )

        return redirect('post', kwargs['id'])
