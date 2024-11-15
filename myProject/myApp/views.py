from django.shortcuts import render
from .models import Profesor

# Create your views here.
def home(request):
    context={}
    return render(request, "myApp/home.html", context)

def lista_profesori(request):
    profesori = Profesor.objects.all()
    return render(request, 'myApp/lista_profesori.html', {'profesori': profesori})