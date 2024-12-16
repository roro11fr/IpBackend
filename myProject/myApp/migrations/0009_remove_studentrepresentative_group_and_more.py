# Generated by Django 5.1.3 on 2024-12-16 11:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0008_alter_teachingstaff_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentrepresentative',
            name='group',
        ),
        migrations.RemoveField(
            model_name='studentrepresentative',
            name='student',
        ),
        migrations.RemoveField(
            model_name='request',
            name='details',
        ),
        migrations.RemoveField(
            model_name='request',
            name='request_date',
        ),
        migrations.RemoveField(
            model_name='request',
            name='request_type',
        ),
        migrations.AddField(
            model_name='request',
            name='destinatar',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='destinatar_requests', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Student', 'Student'), ('Professor', 'Professor'), ('Secretary', 'Secretary'), ('HeadOfDepartment', 'HeadOfDepartment'), ('Other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='request',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='ExamSchedulingRequest',
        ),
        migrations.DeleteModel(
            name='StudentRepresentative',
        ),
    ]
