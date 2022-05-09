from django.contrib.auth import get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView, FormView

from .forms import RegistrationForm, ActivationForm, LoginForm

User = get_user_model()


class RegistrationView(FormView):
    model = User
    form_class = RegistrationForm
    template_name = 'account/registration.html'
    extra_context = {}
    success_url = 'activate/'


class ActivationView(FormView):
    model = User
    form_class = ActivationForm
    template_name = 'account/activation.html'
    extra_context = {}
    success_url = '/success_registration/'


@login_required
def success_registration(request):
    return render(request, 'account/success_registration.html')


class LoginView(FormView):
    model = User
    form_class = LoginForm
    template_name = 'account/login.html'
    extra_context = {}
    success_url = '/success_registration/'

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


def logout_view(request):
    logout(request)
    from django.http import HttpResponse
    return HttpResponse(request.user.is_authenticated)
