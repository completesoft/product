from django.conf.urls import url
from ..views import CvList, CvDetail, CvUpdate, ajax_change_state


app_name = 'manage_form'
urlpatterns = [
    url(r'^$', CvList.as_view(), name="cv_list"),
    url(r'^detail/(?P<person_id>\d+)/$', CvDetail.as_view(), name="cv_detail"),
    url(r'^update/(?P<person_id>\d+)/$', CvUpdate.as_view(), name="cv_update"),
    url(r'^ajax_change_state/(?P<person_id>\d+)/$', ajax_change_state, name="ajax_change_state"),
]
