from django.forms import ValidationError
from django.shortcuts import render
from .models import CustomUser, Professor, Exam, Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, ExamSerializer, RequestSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from .permissions import IsSecretary, IsProfessor, IsStudent, IsStudentRepresentative
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.db import transaction
from rest_framework import status


# Create your views here.
def home(request):
    context={}
    return render(request, "myApp/home.html", context)


def lista_profesori(request):
    profesori = Professor.objects.all()
    return render(request, 'myApp/lista_profesori.html', {'profesori': profesori})


class LoginView(APIView):
    permission_classes = [AllowAny]  # Permite accesul public la acest endpoint

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Permite doar utilizatorilor autentificați să iasă

    def post(self, request):
        # Obține utilizatorul care face cererea
        user = request.user
        
        try:
            # Obține refresh token-ul din request
            token = request.data.get('token')
            
            if not token:
                return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Creează un obiect RefreshToken folosind token-ul primit
            token_obj = RefreshToken(token)
            
            # Obține utilizatorul asociat cu refresh token-ul
            payload = token_obj.payload  # Decodificăm payload-ul din refresh token
            token_user_id = payload.get('user_id')
            # print(f"Token user_id: {token_user_id}, Request user.id: {user.id}")

            # Verificăm dacă user_id din payload corespunde cu utilizatorul care face cererea
            if int(token_user_id) != user.id:  # Comparăm ambele ca integeri
                return Response({"error": "Invalid token for this user"}, status=status.HTTP_400_BAD_REQUEST)

            # Dacă token-ul este valid, marchează-l ca blacklist (invalid)
            token_obj.blacklist()

            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"error": f"Token error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ExamViewSet(ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

    def get_permissions(self):
        """
        Permisiuni bazate pe metoda HTTP.
        - GET: Orice utilizator autentificat.
        - POST, PUT, DELETE: Doar utilizatorii cu rolul 'Secretary'.
        """
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [IsStudentRepresentative()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Salvează examenul doar dacă cererea a fost aprobată de către profesor și secretariat.
        """
        request_data = self.request.data  # Obține datele din cerere

        # Verificați dacă cererea este aprobată de profesor și secretariat
        try:
            request = Request.objects.get(id=request_data.get('request_id'))
            if request.status == 'ApprovedBySecretary':
                serializer.save()  # Salvează examenul
            else:
                raise ValidationError("Cererea nu a fost aprobată de secretariat.")
        except Request.DoesNotExist:
            raise ValidationError("Cererea nu există.")


class CanPostRequest(BasePermission):
    """
    Permisiune care permite POST doar pentru StudentRepresentative, Profesor sau Secretariat.
    """
    def has_permission(self, request, view):
        # Permite POST doar pentru StudentRepresentative, Profesor sau Secretariat
        user_role = request.user.role
        return user_role in ["StudentRepresentative", "Professor", "Secretary"]


class CanDeleteRequest(BasePermission):
    """
    Permisiune care permite DELETE doar pentru Secretariat.
    """
    def has_permission(self, request, view):
        # Permite DELETE doar pentru Secretariat
        return request.user.groups.filter(name="Secretariat").exists()

class RequestListView(APIView):
    """
    View pentru crearea și listarea cererilor de examen.
    """
    def get_permissions(self):
        if self.request.method == "POST":
            return [CanPostRequest()]  # Permite doar utilizatorilor cu rolurile specificate să posteze
        elif self.request.method == "DELETE":
            return [CanDeleteRequest()]  # Permite doar Secretariatului să șteargă cererile
        return [IsAuthenticated()]  # Permite doar autentificarea pentru GET

    def get(self, request):
        """
        Returnează toate cererile de examen.
        """
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Permite crearea unei noi cereri de examen.
        """
        exam_name = request.data.get('exam_name')
        exam_type = request.data.get('exam_type')
        duration = request.data.get('duration')
        department = request.data.get('department')
        room = request.data.get('room')
        scheduled_date = request.data.get('scheduled_date')
        scheduled_time = request.data.get('scheduled_time')
        profesor_nume = request.data.get('proffesor')

        # Verifică dacă numele profesorului a fost furnizat
        if not profesor_nume:
            return Response({"error": "Profesor name is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            last_name, first_name = profesor_nume.split(" ", 1)
        except ValueError:
            return Response({"error": "Profesor name must include both first name and last name."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profesor = CustomUser.objects.get(
                Q(first_name=first_name) & Q(last_name=last_name), 
                role="Professor"
            )
        except CustomUser.DoesNotExist:
            return Response({"error": "Profesor not found or user does not have the 'Professor' role."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        # Creăm cererea fără a crea examenul încă, dar trimitem datele examenului
        request_data = {
            'user': user.id,
            'exam': None,  # Nu asociem examenul încă
            'destinatar': profesor.id,
            'status': 'Pending',
            'exam_details': {  # Transmitem manual datele examenului
                'name': exam_name,
                'exam_type': exam_type,
                'duration': duration,
                'department': department,
                'room': room,
                'scheduled_date': scheduled_date,
                'scheduled_time': scheduled_time,
                'proffesor': profesor.id,
            }
        }

        serializer = RequestSerializer(data=request_data)

        if serializer.is_valid():
            cerere = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def delete(self, request):
        """
        Șterge cererea doar dacă este respinsă (`rejected`).
        """
        try:
            # Presupunem că trimitem ID-ul cererii pentru ștergere
            request_id = request.data.get("id")
            cerere = Request.objects.get(id=request_id)

            if cerere.status == "Rejected":
                cerere.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"detail": "Cererea nu poate fi ștearsă pentru că nu este respinsă."},
                                status=status.HTTP_400_BAD_REQUEST)
        except Request.DoesNotExist:
            return Response({"detail": "Cererea nu a fost găsită."}, status=status.HTTP_404_NOT_FOUND)



class ProfessorRequestsView(APIView):
    """
    Gestionarea cererilor de către profesor.
    """
    permission_classes = [IsProfessor]

    def patch(self, request, request_id):
        """
        Aprobare sau respingere cerere de către profesor.
        """
        try:
            request_obj = Request.objects.get(id=request_id)
        except Request.DoesNotExist:
            return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get("action")

        if action == "approve" and request_obj.status == "Pending":
            request_obj.status = "ApprovedByProfessor"
            request_obj.save()
            return Response({"message": "Request approved by professor."}, status=status.HTTP_200_OK)
        elif action == "reject" and request_obj.status == "Pending":
            request_obj.status = "Rejected"
            request_obj.save()  # Actualizăm statusul
            return Response({"message": "Request rejected."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action or status for this request."}, status=status.HTTP_400_BAD_REQUEST)


class SecretaryRequestsView(APIView):
    permission_classes = [IsAuthenticated, IsSecretary]

    @transaction.atomic
    def patch(self, request, request_id):
        """
        Aprobare sau respingere cerere de către secretar și crearea examenului asociat.
        """
        try:
            request_obj = Request.objects.get(id=request_id)
        except Request.DoesNotExist:
            return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get("action")

        if action == "approve":
            # Validare și aprobare cerere (logică existentă)
            if request_obj.status != 'ApprovedByProfessor':
                return Response({"error": "Request must be approved by the professor first."}, status=status.HTTP_400_BAD_REQUEST)

            # Datele examenului primite de la cererea utilizatorului
            exam_data = request.data.get('exam')

            if not exam_data:
                return Response({"error": "Exam data is required to approve the request."}, status=status.HTTP_400_BAD_REQUEST)

            # Validăm datele examenului
            exam_serializer = ExamSerializer(data=exam_data)
            if not exam_serializer.is_valid():
                return Response(exam_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Creăm examenul în baza de date
            exam = exam_serializer.save()

            # Actualizăm cererea cu examenul și modificăm statusul
            request_obj.exam = exam
            request_obj.status = 'ApprovedBySecretary'
            request_obj.save()

            return Response(
                {
                    "message": "Request approved by secretary and exam created.",
                    "request": RequestSerializer(request_obj).data,
                    "exam": ExamSerializer(exam).data,
                },
                status=status.HTTP_200_OK,
            )

        elif action == "reject":
            # Rejecția cererii
            if request_obj.status in ["Pending", "ApprovedByProfessor"]:
                request_obj.status = "Rejected"
                request_obj.save()

                return Response(
                    {"message": "Request rejected by secretary."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Request cannot be rejected at this stage."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)
