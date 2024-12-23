from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_ROLES = [
        ('Student', 'Student'),
        ('Professor', 'Professor'),
        ('Secretary', 'Secretary'),
        ('HeadOfDepartment', 'HeadOfDepartment'),
        ('StudentRepresentative', 'StudentRepresentative'),
        ('Other', 'Other')
    ]
    
    role = models.CharField(max_length=50, choices=USER_ROLES)
    status = models.CharField(max_length=50, default="Active")

    class Meta:
        db_table = 'tbl_custom_user'

    def __str__(self):
        return self.username

#20. Facultate
class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=50, blank=True)
    long_name = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'tbl_faculty'

    def __str__(self):
        return self.short_name if self.short_name else "Unnamed Faculty"

# 1. Model pentru Departamente
class Department(models.Model):
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    contact_info = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'tbl_department'

    def __str__(self):
        return self.name

# 2. Model pentru Specializări
class Specialization(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    duration = models.IntegerField()  # Durata studiilor în ani
    study_level = models.CharField(max_length=50, choices=[('Bachelor', 'Bachelor'), ('Master', 'Master'), ('PhD', 'PhD')])

    class Meta:
        db_table = 'tbl_specialization'

    def __str__(self):
        return self.name

# 3. Model pentru Grupe
class Group(models.Model):
    name = models.CharField(max_length=50)
    study_year = models.IntegerField()  # Anul de studiu
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    number_of_students = models.IntegerField()

    class Meta:
        db_table = 'tbl_group'

    def __str__(self):
        return self.name



# 5. Model pentru Studenți (extensie a CustomUser)
class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_student'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# 6. Model pentru Profesori
class Professor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)  # Titular sau Asistent
    availability_start = models.DateTimeField(null=True, blank=True)
    availability_end = models.DateTimeField(null=True, blank=True)
    activity = models.TextField()

    class Meta:
        db_table = 'tbl_professor'

    def __str__(self):
        return f"Prof. {self.user.first_name} {self.user.last_name}"

# 7. Model pentru Săli de examen
class Room(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=True, null=True)  # Numele complet al sălii
    short_name = models.CharField(max_length=50, blank=True)  # Numele prescurtat al sălii
    building_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'tbl_room'

    def __str__(self):
        return f"{self.name or 'Unnamed Room'} ({self.building_name})"

# 8. Model pentru Examene
class Exam(models.Model):
    EXAM_TYPES = [
        ('Written', 'Written'),
        ('Oral', 'Oral'),
        ('Mixed', 'Mixed'),
    ]
    proffesor = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPES)
    duration = models.IntegerField()  # Durata examenului în minute
    # department = models.ForeignKey(Department, on_delete=models.CASCADE)
    # room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    department = models.CharField(max_length=50)
    room = models.CharField(max_length=50)

    class Meta:
        db_table = 'tbl_exam'

    def __str__(self):
        return self.name

# 9. Model pentru Cereri de programare a examenelor
class Request(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_requests')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='Pending', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    destinatar = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='destinatar_requests')

    class Meta:
        db_table = 'tbl_request'

    def __str__(self):
        return f"Request for {self.exam.name} by {self.user.username}"

# 10. Model pentru notificări
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=50)
    message = models.TextField()
    status = models.CharField(max_length=50, default='Unread', choices=[('Unread', 'Unread'), ('Read', 'Read')])

    class Meta:
        db_table = 'tbl_notification'

    def __str__(self):
        return f"Notification for {self.user.username}"

# 11. Default_Exams
class DefaultExam(models.Model):
    STATUS_CHOICES = [
        ('pending_confirmation', 'Pending Confirmation'),
        ('confirmed', 'Confirmed'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    course = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    assistant = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True, related_name="assistant_exams")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_default_exam'

    def __str__(self):
        return f"{self.course.name} - {self.scheduled_date} {self.scheduled_time}"

# 12. Professor_Availability
class ProfessorAvailability(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
    ]
    
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    available_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_professor_availability'

    def __str__(self):
        return f"{self.professor} - {self.available_date}"

# 13. Exam_Session_Schedule
class ExamSessionSchedule(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_exam_session_schedule'

    def __str__(self):
        return f"Session from {self.start_date} to {self.end_date}"


# 15. Rescheduling_Requests
class ReschedulingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    new_requested_date = models.DateField()
    new_requested_time = models.TimeField()
    reason = models.TextField()
    initiated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="target_user_requests")
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="processed_by_requests")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_rescheduling_request'

    def __str__(self):
        return f"Rescheduling request for {self.exam}"

# 17. Secretary
class Secretary(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="Active")

    class Meta:
        db_table = 'tbl_secretariat'

    def __str__(self):
        return f"Secretary: {self.user.first_name} {self.user.last_name}"

# 18. DepartamentHead
class DepartmentHead(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default="Active")

    class Meta:
        db_table = 'tbl_department_head'

    def __str__(self):
        return f"Department Head: {self.user.first_name} {self.user.last_name}"

# 19. Cadru Didactic
class TeachingStaff(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50, blank=True, null=True)  # Număr de telefon
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)  # Legătură cu Departament

    class Meta:
        db_table = 'tbl_teaching_staff'

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.department_name})" 