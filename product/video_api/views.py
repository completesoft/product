from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import MotionReg
from .serializers import MotionregSerializer
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.conf import settings
from .forms import VideoRecordFilterForm


@csrf_exempt
@api_view(['POST'])
def recording(request):
    serializer = MotionregSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecordList(ListView):
    template_name = "video_api/record_list.html"
    model = MotionReg
    ordering = "time_start"
    context_object_name = "records"
    filter_form = None
    
    def get(self, request, *args, **kwargs):
        if request.GET:
            self.filter_form = VideoRecordFilterForm(request.GET)
            if self.filter_form.is_valid():
                self.queryset = self.model.objects.filter(**self.filter_form.filter_set())
            else:
                self.queryset = self.model.objects.none()
        else:
            self.filter_form = VideoRecordFilterForm()
        return super(RecordList, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RecordList, self).get_context_data(**kwargs)
        context['filter_form'] = self.filter_form
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return super(RecordList, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)