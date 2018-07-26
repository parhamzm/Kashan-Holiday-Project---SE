from django.conf.urls import url
from .views import TourCategoryListView, TourCategoryDetailView


urlpatterns = [
    url(r'^$', TourCategoryListView.as_view(), name='categories'),
    url(r'^(P<slug>[\w-]+)/$', TourCategoryListView.as_view(), name='category_detail'),
]
