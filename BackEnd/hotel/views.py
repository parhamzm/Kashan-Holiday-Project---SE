from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Hotel

# Create your views here.


class HotelDetailView(DetailView):
    model = Hotel
    template_name='hotel/hotel_detail.html'
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)   
        return context



class HotelListView(ListView):
    model = Hotel
    template_name= 'hotel/hotel_list.html'
    
    #paginate_by=10
    # def get_context_data(self,**kwargs):
    #     context=super().get_context_data(*args,**kwargs)
    #     print('context: ',context)
    #     return context
    
    

