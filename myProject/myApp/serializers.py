from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, Exam, Request, Room


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        refresh = RefreshToken.for_user(user)
        role = user.role
        return {
            'access': str(refresh.access_token),  # Token de acces
            'refresh': str(refresh),             # Token de refresh
            'role': role
        }


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'proffesor', 'name', 'exam_type', 'duration', 'department', 'room', 'scheduled_date', 'scheduled_time']


class RequestSerializer(serializers.ModelSerializer):
    exam_details = serializers.JSONField(write_only=True)  # Acceptăm datele ca JSON la scriere

    class Meta:
        model = Request
        fields = ['id', 'user', 'exam', 'exam_details', 'status', 'destinatar']
        extra_kwargs = {
            'exam': {'required': False},
        }

    def create(self, validated_data):
    # Extragem exam_details din datele validate
        exam_details = validated_data.pop('exam_details', None)

        if exam_details and 'proffesor' in exam_details:
            try:
                # Obține numele complet al profesorului pe baza ID-ului
                profesor_id = exam_details['proffesor']
                profesor = CustomUser.objects.get(id=profesor_id)
                exam_details['proffesor'] = f"{profesor.last_name} {profesor.first_name}"
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError({"proffesor": "Profesorul nu a fost găsit."})

        # Creăm obiectul Request
        request_obj = Request.objects.create(**validated_data)

        # Salvăm exam_details, dacă există
        if exam_details:
            request_obj.exam_details = exam_details
            request_obj.save()

        return request_obj


    def to_representation(self, instance):
        response = super().to_representation(instance)

        # Înlocuim ID-ul destinatarului cu numele complet
        if instance.destinatar:
            response['destinatar'] = f"{instance.destinatar.last_name} {instance.destinatar.first_name}"
        
        # Gestionăm detaliile examenului
        if instance.exam:
            response['exam_details'] = {
                "id": instance.exam.id,
                "name": instance.exam.name,
                "exam_type": instance.exam.exam_type,
                "duration": instance.exam.duration,
                "department": instance.exam.department,
                "room": instance.exam.room,
                "scheduled_date": instance.exam.scheduled_date,
                "scheduled_time": instance.exam.scheduled_time,
            }
        elif hasattr(instance, 'exam_details'):
            response['exam_details'] = instance.exam_details
        else:
            response['exam_details'] = {
                "id": None,
                "name": "No exam assigned",
                "exam_type": None,
                "duration": None,
                "department": None,
                "room": None,
                "scheduled_date": None,
                "scheduled_time": None,
            }
        return response


class CustomUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name}"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'short_name']