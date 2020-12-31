"""ipmd_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from emotions import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.generic.base import TemplateView # new
from django.urls import path, include # new
from django.conf.urls import url
from django_email_verification import urls as mail_urls

urlpatterns = [
    path('ipmd-admin/', admin.site.urls),
 #   path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', views.home),
    path('accounts/', include('accounts.urls')),
    path('submit', views.submit),
    path('faceTracker', views.faceTracker),
    path('overlay', views.overlay),
    path('videosubmit', views.videosubmit),
    path('videolimit', views.videolimit),
    path('results_overlay', views.results_overlay),
    path('home', views.home),
    #path('fail2', views.fail2),
    path('results', views.results),
    path('video', views.video),
    path('forum', views.forum, name='forum'),
    path('delete_thread/<pk>/', views.delete_thread, name='delete_thread'),
    path('forum/<int:thread>/',views.comments),
    path('userVideo', views.userVideo),
    re_path(r'^submit/$', views.submit, name='submit'),
    path('email/', include(mail_urls)),
    path('', include('django.contrib.auth.urls')) #might not be right address
] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
