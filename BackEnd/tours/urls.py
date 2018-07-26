from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.TourListView.as_view(), name='Tour_List'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/$', views.TourDetailView.as_view(), name='Tour_Detail'),
    url(r'^(?P<pk>\d+)/(?P<slug>[\w-]+)/inventory/$', views.TourVariationListView.as_view(), name='Tour_Inventory'),
]
