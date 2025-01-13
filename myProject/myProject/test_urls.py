import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'myProject.settings'  # Replace with your project name
import django
django.setup()

import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from myApp.models import CustomUser, Exam, Request  # Import CustomUser model
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
def test_home_page():
    client = APIClient()
    url = reverse('home')  # Route for home
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_lista_profesori():
    client = APIClient()
    url = reverse('lista_profesori')  # Route for list of professors
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_login():
    client = APIClient()
    user = CustomUser.objects.create_user(username='user', password='password')
    response = client.post('/auth/login/', {'username': 'user', 'password': 'password'})
    assert response.status_code == status.HTTP_200_OK
    # Check for 'access' and 'refresh' keys instead of 'token'
    assert 'access' in response.data
    assert 'refresh' in response.data
    access_token = response.data['access']
    refresh_token = response.data['refresh']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)


@pytest.mark.django_db
def test_logout():
    client = APIClient()
    
    # Creează și autentifică utilizatorul
    user = CustomUser.objects.create_user(username='user', password='password')
    response = client.post('/auth/login/', {'username': 'user', 'password': 'password'})

    # Obține token-ul de acces și refresh token-ul
    access_token = response.data['access']
    refresh_token = response.data['refresh']

    # Setează access_token în header-ul cererii
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    # Cererea pentru logout - trimite refresh token-ul în body
    url = reverse('logout')  # Asigură-te că ai numele corect al rutei de logout
    response = client.post(url, {'token': refresh_token})  # Trimite refresh token-ul în body

    # Verifică dacă statusul răspunsului este 200 OK
    assert response.status_code == status.HTTP_200_OK
    assert response.data['message'] == "Logged out successfully"


@pytest.mark.django_db
def test_get_request_list():
    client = APIClient()

    # Creează și autentifică utilizatorul 'secretariat_user' cu parola 'parola123'
    user = CustomUser.objects.create_user(username='secretariat_user', password='parola123', role='Secretary')
    
    # Autentifică utilizatorul
    response = client.post('/auth/login/', {'username': 'secretariat_user', 'password': 'parola123'})
    access_token = response.data['access']
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    # Cererea pentru lista de cereri
    url = reverse('request-list')  # Asigură-te că ai ruta corectă pentru lista de cereri
    response = client.get(url)

    # Verifică dacă statusul răspunsului este 200 OK
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_professor_requests():
    client = APIClient()

    # Creează și autentifică un utilizator de tip 'Professor' (sau orice alt rol necesar)
    professor = CustomUser.objects.create_user(username='holubiac.iulianstefan@usm.ro', password='cadru', role='Professor')

    # Creează o cerere de test pentru profesor
    exam = Exam.objects.create(
        name="Test Exam", exam_type="Written", duration=60,
        scheduled_date="2025-06-01", scheduled_time="10:00:00",
        department="Computer Science", room="101A"
    )
    request_obj = Request.objects.create(
        user=professor, exam=exam, destinatar=professor,
        status="Pending", exam_details={'name': "Test Exam", 'exam_type': "Written", 'duration': 60}
    )

    # Autentifică utilizatorul
    response = client.post('/auth/login/', {'username': 'holubiac.iulianstefan@usm.ro', 'password': 'cadru'})
    access_token = response.data['access']
    
    # Setează token-ul de acces în antetul cererii
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

    # Verifică URL-ul generat pentru `approveProfessor`
    request_id = request_obj.id  # ID-ul cererii create
    url = reverse('approveProfessor', kwargs={'request_id': request_id})  # Ruta pentru approveProfessor
    print(f"Generated URL: {url}")  # Adaugă acest print pentru debugging

    # Trimite cererea PATCH cu autentificarea corectă
    data = {
        "action": "approve"  # Poți schimba cu "reject" pentru a respinge cererea
    }
    response = client.patch(url, data, format='json')

    # Verifică dacă statusul răspunsului este 200 OK
    assert response.status_code == status.HTTP_200_OK



# @pytest.mark.django_db
# def test_secretary_requests():
#     client = APIClient()

#     # Crează utilizatorii (profesor și secretar)
#     professor = CustomUser.objects.create_user(
#         username='professor@example.com',
#         password='password',
#         role='Professor'
#     )
#     secretary = CustomUser.objects.create_user(
#         username='secretary@example.com',
#         password='password',
#         role='Secretary'
#     )

#     # Crează un examen
#     exam = Exam.objects.create(
#         name="Test Exam",
#         exam_type="Written",
#         duration=60,
#         scheduled_date="2025-06-01",
#         scheduled_time="10:00:00",
#         department="Computer Science",
#         room="101A"
#     )

#     # Crează o cerere aprobată de profesor
#     request_obj = Request.objects.create(
#         user=professor,
#         exam=exam,
#         destinatar=secretary,
#         status="ApprovedByProfessor",
#         exam_details={'name': "Test Exam", 'exam_type': "Written", 'duration': 60}
#     )

#     # Autentifică utilizatorul secretar
#     response = client.post('/auth/login/', {'username': 'secretary@example.com', 'password': 'password'})
#     access_token = response.data['access']
#     client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)

#     # Testează GET cererile aprobate de profesori pentru secretar
#     url = reverse('request-list')  # Înlocuiește cu ruta corectă pentru listarea cererilor
#     response = client.get(url)

#     assert response.status_code == status.HTTP_200_OK
#     assert len(response.data) > 0  # Verificăm că există cereri în răspuns

#     # Testează PATCH pentru aprobarea cererii de către secretar
#     data = {
#         'action': 'approve',
#         'exam': {
#             'name': "Test Exam",
#             'exam_type': "Written",
#             'duration': 60,
#             'scheduled_date': "2025-06-01",
#             'scheduled_time': "10:00:00",
#             'department': "Computer Science",
#             'room': "101A"
#         }
#     }
#     url = reverse('approveSecretary', kwargs={'request_id': request_obj.id})  # Înlocuiește cu ruta corectă
#     response = client.patch(url, data, format='json')

#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['message'] == "Request approved by secretary and exam created."
#     assert 'exam' in response.data
#     assert response.data['request']['status'] == "ApprovedBySecretary"

#     # Testează PATCH pentru respingerea cererii de către secretar
#     data = {'action': 'reject'}
#     response = client.patch(url, data, format='json')

#     assert response.status_code == status.HTTP_200_OK
#     assert response.data['message'] == "Request rejected by secretary and removed."
#     assert not Request.objects.filter(id=request_obj.id).exists()  # Verificăm că cererea a fost ștearsă

