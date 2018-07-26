from django.conf.urls import url
from .views import post_list, post_detail, post_create, post_update, post_delete, PostDetailView

urlpatterns = [
    url(r'^create/$', post_create, name='create'),
    url(r'^$', post_list, name="list"),
    url(r'^(?P<slug>[\w-]+)/$', PostDetailView.as_view(), name="detail"),
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name="update"),
    url(r'^(?P<slug>\d+)/delete/$', post_delete, name='delete')
]
