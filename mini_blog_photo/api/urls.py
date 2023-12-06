

from django.urls import path, include

from api.views import PhotoListView, CommentListCreateView

urlpatterns = [
    path('photos/', PhotoListView.as_view()),
    path('comments/', CommentListCreateView.as_view())
]
