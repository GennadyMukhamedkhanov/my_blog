from django.urls import path
from myblog.views.photo import *
from myblog.views.comment import *
from myblog.views.user import *
from myblog.views.like import *

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('registration/', RegistrationView.as_view(), name='registration'),
    path('authorization/', AuthorizationView.as_view(), name='authorization'),
    path('exit_account/', ExitAccountView.as_view(), name='exit_account'),

    path('personal_account/', PersonalAccount.as_view(), name='personal_account'),
    path('add_photo/', AddPhotoView.as_view(), name='add_photo'),
    path('editing_photo/<int:id>/', EditingPhotoView.as_view(), name='editing_photo'),
    path('editing_description/<int:id>/', EditingDescriptionView.as_view(), name='editing_description'),
    path('del_comment/<int:id_comment>/<int:id_photo>/', DelCommentView.as_view(), name='del_comment'),
    path('editing_comment/<int:id_comment>/<int:id_photo>/', EditingCommentsView.as_view(), name='editing_comment'),

    path('post/<int:id>/', PostDetailView.as_view(), name='post'),
    path('like/<int:id>', LikeView.as_view(), name='like'),
    path('dislike/<int:id>', DislikeView.as_view(), name='dislike'),




]
