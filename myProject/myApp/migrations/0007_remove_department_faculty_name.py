# Generated by Django 5.1.3 on 2024-12-07 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0006_remove_department_faculty_name_department_faculty_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='faculty_name',
        ),
    ]
