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



@csrf_exempt
@api_view(['POST'])
def recording(request):
    print('POST PRINT', request.data)
    serializer = MotionregSerializer(data=request.data)
    if serializer.is_valid():
        print('VALID', serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    print('BAD', serializer.data)
    print('ERROR', serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecordList(ListView):
    template_name = "video_api/record_list.html"
    model = MotionReg
    ordering = "time_start"
    context_object_name = "records"

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_superuser:
            return super(RecordList, self).dispatch(request, *args, **kwargs)
        else:
            return redirect(settings.LOGIN_URL)