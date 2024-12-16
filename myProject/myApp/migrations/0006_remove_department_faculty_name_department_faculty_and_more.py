# Generated by Django 5.1.3 on 2024-12-07 09:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0005_faculty'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myApp.faculty'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='professor',
            name='availability_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='professor',
            name='availability_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]