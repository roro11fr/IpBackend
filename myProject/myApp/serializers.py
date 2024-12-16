from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Exam, Request


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),  # Token de acces
            'refresh': str(refresh),             # Token de refresh
        }


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'proffesor', 'name', 'exam_type', 'duration', 'department', 'room', 'scheduled_date', 'scheduled_time']


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'