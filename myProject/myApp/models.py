from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER_ROLES = [
        ('Student', 'Student'),
        ('Professor', 'Professor'),
        ('Secretary', 'Secretary'),
        ('HeadOfDepartment', 'HeadOfDepartment'),
        ('GroupLeader', 'GroupLeader'),
    ]
    
    role = models.CharField(max_length=50, choices=USER_ROLES)
    status = models.CharField(max_length=50, default="Active")

    class Meta:
        db_table = 'tbl_custom_user'

    def __str__(self):
        return self.username

# 1. Model pentru Departamente
class Department(models.Model):
    name = models.CharField(max_length=255)
    faculty_name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'tbl_department'

    def __str__(self):
        return self.name

# 2. Model pentru Specializări
class Specialization(models.Model):
    name = models.CharField(max_length=255)
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
    status = models.CharField(max_length=50, default="Active")

    class Meta:
        db_table = 'tbl_student'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

# 6. Model pentru Profesori
class Professor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)  # Titular sau Asistent
    availability_start = models.DateTimeField()
    availability_end = models.DateTimeField()
    activity = models.TextField()

    class Meta:
        db_table = 'tbl_professor'

    def __str__(self):
        return f"Prof. {self.user.first_name} {self.user.last_name}"

# 7. Model pentru Săli de examen
class Room(models.Model):
    ROOM_TYPES = [
        ('Lecture Hall', 'Lecture Hall'),
        ('Laboratory', 'Laboratory'),
        ('Amphitheater', 'Amphitheater'),
    ]
    room_number = models.CharField(max_length=50)
    capacity = models.IntegerField()
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)
    location = models.CharField(max_length=255)

    class Meta:
        db_table = 'tbl_room'

    def __str__(self):
        return self.room_number

# 8. Model pentru Examene
class Exam(models.Model):
    EXAM_TYPES = [
        ('Written', 'Written'),
        ('Oral', 'Oral'),
        ('Mixed', 'Mixed'),
    ]
    name = models.CharField(max_length=255)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPES)
    exam_date = models.DateTimeField()
    duration = models.IntegerField()  # Durata examenului în minute
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField()

    class Meta:
        db_table = 'tbl_exam'

    def __str__(self):
        return self.name

# 9. Model pentru Cereri de programare a examenelor
class Request(models.Model):
    REQUEST_TYPES = [
        ('ScheduleRequest', 'Schedule Request'),
        ('RescheduleRequest', 'Reschedule Request'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=50, choices=REQUEST_TYPES)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending', choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    details = models.TextField(null=True, blank=True)

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

# 14. Student_Representative
class StudentRepresentative(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_student_representative'

    def __str__(self):
        return f"{self.student} - {self.group}"

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

# 16. Exam_Scheduling_Requests
class ExamSchedulingRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    requested_date = models.DateField()
    requested_time = models.TimeField()
    exam_type = models.CharField(max_length=10, choices=[('oral', 'Oral'), ('written', 'Written'), ('mixed', 'Mixed')])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        db_table = 'tbl_exam_scheduling_request'

    def __str__(self):
        return f"Scheduling request for {self.group} on {self.requested_date} at {self.requested_time}"
