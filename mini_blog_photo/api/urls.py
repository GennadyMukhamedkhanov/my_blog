

from django.urls import path, include

from api.views import UserCreateView, TokenGetView, PhotoListCreateView, PhotoShowUpdateDeleteView, PersonalAccount,\
    CommentsListCreateUpdateDeleteView, PersonalCommentsUserListUpdateDeleteOnPhoto, AllData


urlpatterns = [
    path('users/', UserCreateView.as_view()),
    path('token/', TokenGetView.as_view()),

    path('photos/', PhotoListCreateView.as_view()),
    path('photos/<int:pk_photo>/', PhotoShowUpdateDeleteView.as_view()),

    path('data_photo/<int:photo_pk>/', CommentsListCreateUpdateDeleteView.as_view()),

    path('personal_account/', PersonalAccount.as_view()),
    path('personal_account_comments/<int:pk_photo>/', PersonalCommentsUserListUpdateDeleteOnPhoto.as_view()),
    path('personal_comments/<int:pk_comments>/', PersonalCommentsUserListUpdateDeleteOnPhoto.as_view()),
    path('personal_account/<int:pk_comments>/', PersonalCommentsUserListUpdateDeleteOnPhoto.as_view()),

    path('all_data/', AllData.as_view())




    # path('photos/<int:pk>/', PhotoPutDelete.as_view()),
    #
    # path('comments/', CommentListCreateView.as_view()),
    # path('comments/<int:pk>/', CommentPutDelete.as_view()),
    #
    # path('likes/', LikeDislikeCreate.as_view()),
    # path('likes/<int:pk>/', LikeDislikePutDelete.as_view())
]
