from django.shortcuts import render, redirect
from django.views.generic import CreateView

from .forms import CreateAnnouncementForm
from .models import Announcement


def main_view(request):
    announcements = Announcement.objects.all()
    print(announcements)

    return render(request, 'product/main.html', context={'announcements': announcements})


class CreateAnnouncementView(CreateView):
    model = Announcement
    form_class = CreateAnnouncementForm
    extra_context = {'announcements': Announcement.objects.all()}
    template_name = 'product/create.html'
    success_url = '/announcements/'

    # def create(self, request):
    #     data = request.data
    #     form = CreateAnnouncementForm(data=data)
    #     if form.is_valid():
    #         form.create()




# def create(request):
#     if request.method == 'POST':
#         form = CreateAnnouncementForm(request.POST)
#         if form.is_valid():
#             print('----------------')
#             form.save()
#
#
#     form = CreateAnnouncementForm()
#     data = {
#         'form': form,
#     }
#     return render(request, 'product/create.html', data)
#
#
# def add_image(request):
#
#     return render(request, 'product/add_mage.html')
