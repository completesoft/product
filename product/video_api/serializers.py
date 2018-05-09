from rest_framework import serializers
from .models import MotionReg


class MotionregSerializer(serializers.ModelSerializer):

    time_start = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'])

    class Meta:
        model = MotionReg
        fields = ('place_id', 'time_start', 'duration')