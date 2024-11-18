from . import views
from django.urls import path
from .views import LoginView, LogoutView


urlpatterns = [
    path("", views.home, name='home'),
    path('profesori/', views.lista_profesori, name='lista_profesori'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
]
