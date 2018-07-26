"""holiday URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from cart.views import CartView, CartBadgeCountView, CartView2, CartCheckoutView, CheckoutFinalView
from attractions.views import ContactView, AboutView, Index_Page
from django.conf import settings
from django.conf.urls.static import static
from order.views import (
                    AddressSelectFormView, 
                    UserAddressCreateView, 
                    OrderList, 
                    OrderDetail)

urlpatterns = [
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^$', Index_Page, name='home'),
    # url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^restaurants/', include('restaurants.urls', namespace='restaurants')),
    url(r'^hotel/', include('hotel.urls', namespace='hotel')),
    # url(r'^restaurants/create/$', RestaurantCreateView.as_view(), name='restaurants-create'),
    # url(r'^restaurants/$', RestaurantListView.as_view(), name='restaurants-list'),
    # url(r'^restaurants/(?P<pk>\w+)/$', RestaurantDetailView.as_view(), name='restaurant-detail'),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
    url(r'^accounts/', include('accounts.urls', namespace='account')),
    url(r'^tours/', include('tours.urls', namespace='tours')),
    url(r'^tours/categories', include('tours.urls_categories', namespace='categories')),
    url(r'^cart-old/$', CartView.as_view(), name='cart-old'),
    url(r'^orders/$', OrderList.as_view(), name='order'),
    url(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),
    url(r'^cart/$', CartView2.as_view(), name='cart'),
    url(r'^blog/posts/', include("blog.urls", namespace="blog")),
    url(r'^account/', include('registration.backends.default.urls')),
    url(r'^cart/count/$', CartBadgeCountView.as_view(), name='cart_badge'),
    url(r'^checkout/$', CartCheckoutView.as_view(), name='checkout'),
    url(r'^checkout/address/$', AddressSelectFormView.as_view(), name='order_address'),
    url(r'^checkout/address/add/$', UserAddressCreateView.as_view(), name='user_address_create'),
    url(r'^checkout/final/$', CheckoutFinalView.as_view(), name='checkout_final'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)