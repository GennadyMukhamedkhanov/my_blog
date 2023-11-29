

from django.urls import path, include

from api.views import PhotoListView

urlpatterns = [
    path('photos/', PhotoListView.as_view())
]
