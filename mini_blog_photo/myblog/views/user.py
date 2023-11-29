from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View
from myblog.services.user.user import *


class RegistrationView(View):
    def get(self, request):
        return render(request, 'myblog/registration.html')

    def post(self, request):
        UserRegistrationService.execute(
            {
                'username': request.POST['login'],
                'password': request.POST['password'],
                'phone': request.POST['phone'],

            }
        )

        return redirect('index')


class AuthorizationView(View):
    def get(self, request):
        return render(request, 'myblog/authorization.html')

    def post(self, request):
        user = UserAuthorizationService.execute(
            {
                'username': request.POST['login'],
                'password': request.POST['password'],
                'request': {'data': request},

            }
        )

        if user is not None:
            login(request, user)
            return redirect('index')
        return render(request, 'myblog/authorization.html', context={
            'error': 'Попробуйте снова! Возможно вы не зарегистрированы!'
        })


class ExitAccountView(View):
    def get(self, request):
        logout(request)
        return redirect('index')


class PersonalAccount(View):
    def get(self, request):
        data = UserPersonalAccountService.execute(
            {
                'user_id': request.user.id,
            }
        )

        return render(request, 'myblog/personal_account.html',
                      context={'like': data['user'].likes_count,
                               'dislike': data['user'].dislikes_count,
                               'sumlike': data['user'].sum_likes,
                               'count_comment': data['user'].comments_count,
                               'my_photo': data['my_photo']}
                      )
