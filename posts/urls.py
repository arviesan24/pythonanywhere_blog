from django.conf.urls import url
from posts.views import (post_create,
                         post_detail,
                         post_list,
                         post_update,
                         post_delete)
from . import views

urlpatterns = [
    #url(r'^', views.login, name='login'),
    #url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^$', post_list, name='list'), #connected to index.html
    url(r'^create/$', post_create, name='create'), #connected to post_form.html
    url(r'^(?P<slug>[\w-]+)/$', post_detail, name='detail'), #add name to make urls more dynamic instead of hardcoding--connected to post_detail.html
    url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),

]

#next episode 13