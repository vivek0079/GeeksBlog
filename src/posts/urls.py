from django.conf.urls import url
from django.contrib import admin

#import the views to use them
from . import views

app_name = 'post'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^posts/$', views.post_list, name='list'),
    url(r'^create/$', views.post_create, name='create'),
    url(r'^posts/(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
    url(r'^posts/(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
    url(r'^posts/(?P<slug>[\w-]+)/delete/$', views.post_delete, name='delete'), 
]
