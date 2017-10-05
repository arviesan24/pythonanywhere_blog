"""stories URL Configuration

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
from django.conf import settings
from django.conf.urls import url, include  #import include to connect it to the other app
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views

from accounts.views import (login_view, register_view, logout_view)

urlpatterns = [
    #url(r'^', views.login, name='login'),
    #url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^admin/', admin.site.urls, name='adminpage'),
    url(r'^comments/', include("comments.urls", namespace='comments')),

    url(r'^login/', login_view, name='login'),
    url(r'^register/', register_view, name='register'),
    url(r'^logout/', logout_view, name='logout'),

    #reset password URLS
    url(r'^reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',  #include the additional subfolder (registration) of templates so django can find it
            email_template_name='registration/password_reset_email.html',
            subject_template_name='registration/password_reset_subject.txt'
        ),
        name='password_reset'),
    url(r'^reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'),

    url(r'^reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'),

    #END OF reset password URLS


    url(r'^', include("posts.urls", namespace='posts')),  #namespace for set of urls to avoid conflict if several apps has same url name

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    #2:32 mins