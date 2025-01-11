from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView, LogoutView, ExamViewSet, RequestListView, ProfessorRequestsView, SecretaryRequestsView


router = DefaultRouter()
router.register(r'exams', ExamViewSet, basename='exam')  # Creează rute automate pentru `ExamViewSet`


urlpatterns = [
    path("", views.home, name='home'),
    path('profesori/', views.lista_profesori, name='lista_profesori'),
    path('auth/login/', LoginView.as_view(), name='login'), 
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('requests/', RequestListView.as_view(), name='request-list'),
    path('requests/approveProfessor/<int:request_id>/', ProfessorRequestsView.as_view(), name='approveProfessor'),
    path('requests/approveSecretary/<int:request_id>/', SecretaryRequestsView.as_view(), name='approveSecretary'),
]
