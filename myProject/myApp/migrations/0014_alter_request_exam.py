# Generated by Django 5.1.3 on 2024-12-24 19:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0013_alter_request_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='exam',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myApp.exam'),
        ),
    ]
