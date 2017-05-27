from django.conf.urls import url

from . import views
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
 
app_name = 'mainapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^store/$', views.store, name='store'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', auth_views.logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^addToCart/$', views.addToCart, name='addToCart'),
    url(r'^deleteFromCart/$', views.deleteFromCart, name='deleteFromCart'),
    url(r'^product/$', views.product, name='product'),
    url(r'^manager/$', views.manager, name='manager'),
    url(r'^deleteProduct/$', views.deleteProduct, name='deleteProduct'),
    url(r'^addProduct/$', views.addProduct, name='addProduct'),
    url(r'^updateProduct/(?P<item_id>[0-9]+)$', views.updateProduct, name='updateProduct'),
    url(r'^confirm/$', views.confirm, name='confirm'),
]