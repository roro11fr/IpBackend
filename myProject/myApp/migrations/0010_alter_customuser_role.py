# Generated by Django 5.1.3 on 2024-12-23 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0009_remove_studentrepresentative_group_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('Student', 'Student'), ('Professor', 'Professor'), ('Secretary', 'Secretary'), ('HeadOfDepartment', 'HeadOfDepartment'), ('StudentRepresentative', 'StudentRepresentative'), ('Other', 'Other')], max_length=50),
        ),
    ]