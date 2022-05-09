import re

from allauth.account.forms import SignupForm
from django import forms
# from django.contrib.auth import get_user_model
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError
from account import models


User = get_user_model()


class RegistrationForm(forms.ModelForm, SignupForm):
    class Meta:
        model = User
        # exclude = ['is_staff', 'is_active', 'activation_code', 'last_login', 'is_superuser', 'groups',
        #            'user_permissions', 'first_name', 'last_name', 'email', 'active', 'date_joined', 'bebebe']
        fields = ['phone', 'username', 'password']

        widgets = {
            # 'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            # 'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            # 'password': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'пароль'}),
            # 'password_confirmation': forms.TextInput(attrs={'class': 'form-control',
            # 'placeholder': 'Подтверждение пароля'})
        }

    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
                            max_length=20, required=True)
    # username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
    #                            required=True)
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Пароль'}),
                               min_length=6, required=True)
    password_confirmation = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Подтверждение пароля'}),
                                            min_length=6, required=True)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
                           required=True)

    # def clean_phone(self, phone):
    #     import re
    #     re.sub('[^0-9]', '', phone)
    #     if phone.startswith('0'):
    #         phone = f'+996{phone[1:]}'
    #     elif not phone.statrswith('+'):
    #         phone = f'+{phone}'
    #     if len(phone) != 13 and not phone.statrswith('+996'):
    #         raise ValidationError('Неверный формат номера')
    #     if User.objects.filter(phone=phone).exists():
    #         raise ValidationError('Аккаунт с таким номером уже существует')
    #     return phone

    def clean(self):
        from django.utils.crypto import get_random_string
        from django.conf import settings
        from twilio.rest import Client
        from twilio.http.http_client import TwilioHttpClient
        import os
        import re
        phone = self.cleaned_data['phone']
        # username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        print('--------------------')
        re.sub('[^0-9]', '', phone)
        if phone.startswith('0'):
            phone = f'+996{phone[1:]}'
        if not phone.startswith('+'):
            phone = f'+{phone}'
        if len(phone) != 13:
            raise ValidationError('Неверный формат номера')
        user = models.User
        print(user.objects.filter(phone=phone).exists())
        if user.objects.filter(phone=phone).exists():
            raise ValidationError('Аккаунт с таким номером уже существует')
        if password != password_confirmation:
            raise ValidationError('Пароли не совпадают')
        self.cleaned_data.pop('password_confirmation')
        # self.cleaned_data.pop('email')
        self.cleaned_data['phone'] = phone
        self.cleaned_data['username'] = self.cleaned_data.pop('name')
        print(self.cleaned_data)


        # def save(self, request):
        #     user = super(RegistrationForm, self).save()
        #     user.phone = self.cleaned_data['phone']
        #     user.name = self.cleaned_data['name']
        #     user.password = self.cleaned_data['password']
        #     user.save()
        # You must return the original result.
        # print('-----')
        # user_local = get_user_model()
        user = models.User.objects.create_user(**self.cleaned_data)
        # USER = User()
        # user.save_activation_code(code)
        user.create_activation_code()
        user.send_activation_sms()
        # code = get_random_string(6, '0123456789')
        # message = f'Ваш код подтверждения: {code}'
        # client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH_TOKEN)
        # client.messages.create(body=message, from_=settings.TWILIO_PHONE_NUMBER, to=phone)


class ActivationForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'activation_code', 'last_login', 'is_superuser', 'groups',
                   'user_permissions', 'username', 'first_name', 'last_name', 'email', 'active', 'date_joined', 'password']

    code = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Код активации'}),
                           max_length=6, min_length=6, required=True)

    # def clean_code(self, code):
    #     if not User.objects.filter(activation_code=code).exists():
    #         raise ValidationError("Неправильный код")
    #     return code

    def clean(self):
        print('-------')
        print(self.cleaned_data)
        code = self.cleaned_data['code']
        if not models.User.objects.filter(activation_code=code).exists():
            raise ValidationError("Неправильный код")

        user = models.User.objects.get(activation_code=code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        self.get_context()


class LoginForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.request = request

    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'activation_code', 'last_login', 'is_superuser', 'groups',
                   'user_permissions', 'username', 'first_name', 'last_name', 'email', 'active', 'date_joined',
                   ]
    #
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
                            max_length=20, required=True)
    password = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Пароль'}),
                               min_length=6, required=True)
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Имя'}),
                           required=True)

    def clean(self):
        print('-----')
        print(self.cleaned_data)
        user = self.request.user
        print(user)
        print(user.is_authenticated)
        phone = self.cleaned_data['phone']
        password = self.cleaned_data['password']
        username = self.cleaned_data['name']
        re.sub('[^0-9]', '', phone)
        if phone.startswith('0'):
            phone = f'+996{phone[1:]}'
        if not phone.startswith('+'):
            phone = f'+{phone}'
        # if len(phone) != 13:
        #     raise ValidationError('Неверный формат номера')
        # print(phone)
        # user = models.User.objects.get(phone=phone)
        # if not user.is_active:
        #     raise ValidationError('Пользователь не активен')
        # if not user.check_password(password):
        #     raise ValidationError('Неверный пароль')
        # print(phone)
        print(user)
        print(user.is_anonymous)
        if phone and password:
            if not user.is_authenticated:
                user = authenticate(username=phone, password=password, request=self.request)
                print(user)
                if not user:
                    raise ValidationError('Неверные телефон или пароль')
            login(self.request, user)
        else:
            raise ValidationError('Телефон и пароль обязательны')
        # print(user.is_authenticated)


