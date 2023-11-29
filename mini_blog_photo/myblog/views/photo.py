from django.shortcuts import render, redirect
from django.views import View

from myblog.services.photo.photo import *


class IndexView(View):
    def get(self, request):
        photo_data = PhotoIndexService.execute({})
        return render(request, 'myblog/index.html', context={'photo_data': photo_data})

    def post(self, request):
        photo_data = PhotoSearchService.execute(
            {
                'name_photo': request.POST['search'],
            }
        )
        return render(request, 'myblog/index.html', context={'photo_data': photo_data})


class PostDetailView(View):
    def get(self, request, id):
        data = PhotoDetailService.execute(
            {
                'id': id,
                "user_id": request.user.id if isinstance(request.user.id, int) else 0,

            }
        )

        return render(request, 'myblog/detail.html', context={'data': data['photo'],
                                                              'comments': data['comments'],
                                                              'like': data['photo'].like,
                                                              'dislike': data['photo'].dislike,
                                                              'my_like': data.get('my_like'),
                                                              'my_dislike': data.get('my_dislike')})

    def post(self, request, **kwargs):
        PhotoNewCommentService.execute(
            {
                'id_photo': kwargs['id'],
                'id_user': request.user.id,
                'text': request.POST['text'] if request.POST['text'] else 1
            }
        )

        return redirect('post', kwargs['id'])


class AddPhotoView(View):
    def get(self, request):
        return render(request, 'myblog/add_photo.html')

    def post(self, request):
        PhotoCreateService.execute(
            {
                'title': request.POST['title'],
                'description': request.POST['description'],
                'user': request.user,

            },
            {
                'img': request.FILES['img'],
            }
        )
        # Файлы передаются вторым словарем

        return redirect('/')


class EditingPhotoView(View):
    def get(self, request, **kwargs):
        data = PhotoEditingService.execute(
            {
                'id_photo': kwargs['id'],
                'all_comments_user': request.user.comments,
                'user': request.user,
            }
        )

        return render(request, 'myblog/editing_photo.html',
                      context={'photo': data['photo'], 'comments': data['all_comments']})

    def post(self, request, id):
        PhotoDeleteService.execute(
            {'id_photo': id},
        )

        return redirect('personal_account')


class EditingDescriptionView(View):
    def get(self, request, **kwargs):
        DescriptionEditingService.execute(
            {
                'id_photo': kwargs['id'],
                'new_text': request.GET['title'] if request.GET['title'] else 1,
                'new_description': request.GET['description'] if request.GET['description'] else 1,

            }
        )

        return redirect('editing_photo', kwargs['id'])
