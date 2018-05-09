from django.conf.urls import url, include
from .views import CvList, CvDetail, CvUpdate, person, server_response


# app_name = 'candidate'

fill_form = [
    url(r'^$', person, name='index'),
    url(r'^check/$', server_response, name='server_response'),
]


manage_form = [
    url(r'^$', CvList.as_view(), name="cv_list"),
    url(r'^detail/(?P<person_id>\d+)/$', CvDetail.as_view(), name="cv_detail"),
    url(r'^update/(?P<person_id>\d+)/$', CvUpdate.as_view(), name="cv_update"),
]


urlpatterns = [
    url(r'^form-(?P<loc_id>\d+)/', include(fill_form)),
    url(r'^cvmanage/', include(manage_form)),
]