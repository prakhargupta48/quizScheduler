# Generated by Django 5.1.1 on 2024-10-02 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='QuizSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(max_length=100)),
                ('quiz_date', models.DateField()),
                ('quiz_time', models.TimeField()),
                ('faculty_1', models.CharField(max_length=100)),
                ('faculty_2', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UploadedFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_timetable', models.FileField(upload_to='uploads/')),
                ('faculty_file', models.FileField(upload_to='uploads/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
