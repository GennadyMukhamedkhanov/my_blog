from django.shortcuts import redirect, render
from django.views import View

from myblog.models import Comment, Photo
from myblog.services.comment.comment import *


class DelCommentView(View):
    def get(self, request, **kwargs):
        CommentDelService.execute(
            {
                'id_comment': kwargs['id_comment'],
            }
        )
        return redirect('editing_photo', kwargs['id_photo'])


class EditingCommentsView(View):
    def get(self, request, **kwargs):
        data = CommentsEditingService.execute(
            {
                'id_photo': kwargs['id_photo'],
                'id_comment': kwargs['id_comment'],
            }
        )

        return render(request, 'myblog/editing_comments.html', context={
            'photo': data['photo'],
            'comment': data['comment']
        })

    def post(self, request, **kwargs):
        CommentsNewService.execute(
            {
                'new_comment': request.POST['new_text'],
                'id_comment': kwargs['id_comment'],
            }
        )

        return redirect('editing_photo', kwargs['id_photo'])
