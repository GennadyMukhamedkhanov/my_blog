

from django.urls import path, include

from api.views import *
from rest_framework import routers

# router = routers.SimpleRouter()
# router.register(r'photos', PhotoViewSet)

urlpatterns = [
    #path('', include(router.urls)),

    # path('photos/', PhotoViewSet.as_view({'get':'list', 'post':'create'})),
    #path('photos/<int:pk>/', PhotoViewSet.as_view({'put':'update', 'delete':'destroy'})),
    path('photos/', PhotoListCreateView.as_view()),
    path('photos/<int:pk>/', PhotoPutDelete.as_view()),

    path('comments/', CommentListCreateView.as_view()),
    path('comments/<int:pk>/', CommentPutDelete.as_view()),

    path('likes/', LikeDislikeCreate.as_view()),
    path('likes/<int:pk>/', LikeDislikePutDelete.as_view())
]
