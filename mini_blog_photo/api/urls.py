

from django.urls import path, include

from api.views import *


urlpatterns = [
    path('users/', UserCreateView.as_view()),

    path('photos/', PhotoListCreateView.as_view()),

    path('personal_account/<int:pk>/', PersonalAccount.as_view()),
    path('personal_account/create_photo/<int:user_pk>/', CreateUpdateDeletePhohoUser.as_view()),
    path('personal_account/update_delete_photo/<int:pk>/', CreateUpdateDeletePhohoUser.as_view()),

    path('comments_photo/<int:photo_pk>/', ListCommentsLikePhoto.as_view()),
    path('comments_photo/<int:photo_pk>/', ListCommentsLikePhoto.as_view()),

    # path('photos/<int:pk>/', PhotoPutDelete.as_view()),
    #
    # path('comments/', CommentListCreateView.as_view()),
    # path('comments/<int:pk>/', CommentPutDelete.as_view()),
    #
    # path('likes/', LikeDislikeCreate.as_view()),
    # path('likes/<int:pk>/', LikeDislikePutDelete.as_view())
]
