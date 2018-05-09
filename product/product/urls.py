"""form URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    url(r'^login/', login, {'template_name': 'login_form.html'}, name="login"),
    url(r'^logout/', logout_then_login, name="logout"),
    url(r'^form-(?P<loc_id>\d+)/', include('job.urls.fill_form')),
    url(r'^cvmanage/', include('job.urls.manage_form')),
    url(r'^admin/', admin.site.urls),
    url(r'^video_api/', include('video_api.urls')),
]

