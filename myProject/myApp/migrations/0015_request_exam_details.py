# Generated by Django 5.1.3 on 2025-01-11 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0014_alter_request_exam'),
    ]

    operations = [
        migrations.AddField(
            model_name='request',
            name='exam_details',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
