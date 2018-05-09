from django.conf.urls import url
from .views import recording, RecordList

app_name = 'video_api'

urlpatterns = [
    url(r'^recording/$', recording, name='recording'),
    url(r'^report/$', RecordList.as_view(), name='record_list'),
]