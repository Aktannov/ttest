from django import forms
from django.contrib.auth import get_user_model

from .models import Announcement


User = get_user_model()


class CreateAnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок обьявления'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
            'price': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цена'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            # 'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Пользователь'}),
            # 'image': forms.Ima(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Состояние'}),
            'delivery': forms.Select(attrs={'class': 'form-control'}),
        }

    # def clean(self):
    #     print('----------------')
        # validated_data['image'] = self.context.get('request').image
        # return super().create(validated_data)
