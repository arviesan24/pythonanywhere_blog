from django.conf.urls import url
from comments.views import (comment_thread,
                            comment_delete,
                         )
from . import views

urlpatterns = [
    #url(r'^$', post_list, name='list'), #connected to index.html
    #url(r'^create/$', post_create), #connected to post_form.html
    url(r'^(?P<id>\d+)/$', comment_thread, name='thread'), #add name to make urls more dynamic instead of hardcoding--connected to post_detail.html

    url(r'^(?P<id>\d+)/delete/$', comment_delete, name="delete"),

]