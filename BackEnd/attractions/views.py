from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
from tours.models import Tour
from hotel.models import Hotel
from attractions.models import Gallery
# Create your views here.


def Index_Page(request):
    tours= Tour.published.order_by('?')[:6]
    hotels = Hotel.published.order_by('?')[:3]
    attractions_photo = Gallery.objects.order_by('?')[:5]

    return render(request, 'index.html', {'tours': tours, 'hotels': hotels, 'attractions_photo': attractions_photo})


class AboutView(TemplateView):
    
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'





