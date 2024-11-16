from django.shortcuts import render
from .models import Professor
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

# Create your views here.
def home(request):
    context={}
    return render(request, "myApp/home.html", context)

def lista_profesori(request):
    profesori = Professor.objects.all()
    return render(request, 'myApp/lista_profesori.html', {'profesori': profesori})

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = request.data.get('token')
            token_obj = RefreshToken(token)
            token_obj.blacklist()  # Invalidăm token-ul
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
