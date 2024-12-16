from django.shortcuts import render
from .models import Professor, Exam, Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, ExamSerializer, RequestSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.exceptions import TokenError
from .permissions import IsSecretary
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


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
            return [IsSecretary()]
        return [IsAuthenticated()]


class RequestListView(APIView):
    def get(self, request):
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)