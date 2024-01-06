

from django.urls import path, include

from api.views import UserCreateView, TokenGetView, PhotoListCreateView, PhotoShowUpdateDeleteView, PersonalAccount,\
    PhotoShowPersonalAccount,  CommentsUpdateDeleteView, CommentCreateView


urlpatterns = [
    # Users
    path('users/', UserCreateView.as_view()),
    path('token/', TokenGetView.as_view()),
    path('personal_account/', PersonalAccount.as_view()),
    # Photos
    path('photos/', PhotoListCreateView.as_view()),
    path('photos/<int:pk_photo>/', PhotoShowUpdateDeleteView.as_view()),
    path('photos/<int:pk_photo>/personal_account/', PhotoShowPersonalAccount.as_view()),
    # Comments
    path('photos/<int:pk_photo>/comments/', CommentCreateView.as_view()),
    path('comments/<int:pk_comments>/', CommentsUpdateDeleteView.as_view()),

    #path('all_data/', AllData.as_view())




    # path('photos/<int:pk>/', PhotoPutDelete.as_view()),
    #
    # path('comments/', CommentListCreateView.as_view()),
    # path('comments/<int:pk>/', CommentPutDelete.as_view()),
    #
    # path('likes/', LikeDislikeCreate.as_view()),
    # path('likes/<int:pk>/', LikeDislikePutDelete.as_view())
]
