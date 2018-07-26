from django.conf.urls import url
from django.contrib.auth.views import login, logout
# from django.auth.views import logout
from . import views

app_name = 'accounts'

urlpatterns = [
    #url(r'^login/$','django.contrib.auth.views.login',name='login'),
    #url(r'^login/$', login , name='login'),
    #url(r'^logout/$', logout ,name='logout'),
    url(r'^login/$', views.login, name='login'),
    url(r'^signup/$', views.register, name='signup'),
    url(r'^logout/$', logout,
                        {'next_page': '/'}, name='logout'),
]
