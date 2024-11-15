from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name='home'),
    path('profesori/', views.lista_profesori, name='lista_profesori'),
]
