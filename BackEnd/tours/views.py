from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render
from django.http import Http404
from django.db.models import Q
from django.utils import timezone
import datetime
# Create your views here.
# class
from .forms import TourVariationInventoryForm, TourVariationInventoryFormSet
from .models import Tour, TourVariation, TourCategory
from attractions.models import Gallery
from .mixins import StaffRequiredMixin, LoginRequiredMixin


class TourCategoryListView(ListView):
    model = TourCategory
    queryset = TourCategory.objects.all()


class TourCategoryDetailView(DetailView):
    model = TourCategory

    def get_context_data(self, *args, **kwargs):
        context = super(TourCategoryDetailView, self).get_context_data(*args, **kwargs)
        obj = self.get_object()
        tours_set = obj.tour_set.all()
        default_tours = obj.default_category.all()
        tours = (tours_set | default_tours).distinct()
        context["tours"] = tours


class TourVariationListView(StaffRequiredMixin, ListView):
    model = TourVariation
    queryset = TourVariation.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(TourVariationListView, self).get_context_data(*args, **kwargs)
        context["formset"] = TourVariationInventoryFormSet(queryset=self.get_queryset())
        return context
    # template_name = "tour_list.html"

    def get_queryset(self, *args, **kwargs):
        tour_pk = self.kwargs.get("pk")
        queryset = TourVariation.objects.all()
        if tour_pk:
            tour = get_object_or_404(Tour, pk=tour_pk)
            queryset = TourVariation.objects.filter(tour=tour)
        return queryset

    def post(self, request, *args, **kwargs):
        formset = TourVariationInventoryFormSet(request.POST, request.FILES)
        # print("Result Valid => ", formset.is_valid())
        # print(request.POST)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                # print("Title => ", new_item)
                if new_item.title:
                    # print("heloooooo")
                    tour_pk = self.kwargs.get("pk")
                    print("Primary key = > ", tour_pk)
                    tour = get_object_or_404(Tour, pk=tour_pk)
                    new_item.tour = tour
                    new_item.save()
                messages.success(request, "Your inventory and pricing has been Updated!!!")
            # print("helloo")
                return redirect("/tours")
        # print(request.POST)
        raise Http404


class TourListView(ListView):
    model = Tour
    queryset = Tour.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(TourListView, self).get_context_data(*args, **kwargs)
        context["now"] = timezone.now()
        context["query"] = self.request.GET.get("q")
        return context
    # template_name = "tour_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(TourListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return qs


class TourDetailView(DetailView):
    model = Tour
    # template_name = "detail_tour.html"



# def product_detail_view_func(request, id):
#     tour_instance = Tour.objects.get(id=id)
#     template = "pagetour/tour_detail.html"
#     context = {
#         "object": tour_instance
#     }
#     return render(request, template, context)

def List_Tours(request):
    # query example =>blog.published.filter(title__startswith='Who')
    Today = datetime.date.today()
    # Day_ago = Today -datetime.timedelta(days=2)
    List_tour = Tour.published.order_by('?')[:6]
    Random_photo = Gallery.objects.order_by('?')[:6]
    return render(request,'tour/tour.html',{'List_tour':List_tour,'Random_photo':Random_photo})

    
def Details_Tours(request,id, slug):
    tour = get_object_or_404(Tour,id=id,slug=slug,available=True)
    #
    return render (request, 'tour/detail_tour.html',{'tour':tour})


