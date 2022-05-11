from django.urls import path

from .views import RegistrationView, ActivationView, success_registration, LoginView, logout_view

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activate/', ActivationView.as_view()),
    path('success_registration/', success_registration),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
]
