from django.contrib import admin
from .models import Exam
# Register your models here.


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'exam_date', 'duration', 'department', 'room')
    search_fields = ('name', 'exam_type')
    list_filter = ('exam_type', 'exam_date', 'department')