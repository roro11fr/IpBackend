from django.contrib import admin
from .models import Exam
# Register your models here.


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'proffesor', 'exam_type', 'scheduled_date', 'scheduled_time', 'duration', 'department', 'room')
    search_fields = ('name', 'exam_type', 'proffesor', 'room')
    list_filter = ('exam_type', 'scheduled_date', 'department', 'proffesor', 'room')