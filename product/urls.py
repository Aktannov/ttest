from django.urls import path

from .views import main_view, CreateAnnouncementView

urlpatterns = [
    path('', main_view, name='main_view'),
    path('create/', CreateAnnouncementView.as_view(), name='create'),
]
