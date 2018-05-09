from django.conf.urls import url
from ..views import person, server_response


app_name = 'fill_form'
urlpatterns = [
    url(r'^$', person, name='index'),
    url(r'^check/$', server_response, name='server_response'),
]