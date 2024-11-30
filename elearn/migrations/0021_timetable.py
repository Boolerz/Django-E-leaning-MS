# Generated by Django 5.1.3 on 2024-11-29 14:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearn', '0020_lesson'),
    ]

    operations = [
        migrations.CreateModel(
            name='Timetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(max_length=20)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('location', models.CharField(blank=True, max_length=100)),
                ('google_meet_link', models.URLField(blank=True, null=True)),
                ('instructor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elearn.instructor')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elearn.course')),
            ],
        ),
    ]
