from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, primary_key=True)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    DELIVERY_CHOICES = [
        ('paid', 'Платная доставка'),
        ('free', 'Бесплатная доставка'),
        ('pickup', 'Самовывоз')
    ]
    CONDITION_CHOICES = [
        ('used', 'Б/у'),
        ('new', 'Новое'),
        ('perfect', 'Идеальное')
    ]
    title = models.CharField(max_length=50)
    text = models.TextField()
    price = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_name='announcements')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='announcements')
    image = models.ImageField(upload_to='announcements/', null=True, blank=True)
    condition = models.CharField(max_length=7, choices=CONDITION_CHOICES)
    delivery = models.CharField(max_length=6, choices=DELIVERY_CHOICES)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Обьявление'
        verbose_name_plural = 'Обьявления'

