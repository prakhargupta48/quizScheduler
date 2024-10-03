from django.db import models

class UploadedFile(models.Model):
    class_timetable = models.FileField(upload_to='uploads/')
    faculty_file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class QuizSchedule(models.Model):
    subject_name = models.CharField(max_length=100)
    quiz_date = models.DateField()
    quiz_time = models.TimeField()
    faculty_1 = models.CharField(max_length=100)
    faculty_2 = models.CharField(max_length=100)
