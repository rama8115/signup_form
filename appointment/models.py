from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, time, timedelta

User = get_user_model()

class Appointment(models.Model):
    SPECIALITY_CHOICES = (
        ('cardiology','Cardiology'),
        ('dermatology','Dermatology'),
        ('neurology','Neurology'),
        ('pediatrics','Pediatrics'),
        ('orthopedics','Orthopedics'),
        ('ophthalmology','Ophthalmology'),
        ('general Practice','General Practice'),
        ('gastroenterology','Gastroenterology'),
        ('psychiatry','Psychiatry'),
        ('pndocrinology','Endocrinology'),
    )
    patient = models.ForeignKey(User, related_name='appointments_as_patient', on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, related_name='appointments_as_doctor', on_delete=models.CASCADE)
    speciality = models.CharField(max_length=40,choices=SPECIALITY_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.end_time = (datetime.combine(datetime.min, self.start_time) + timedelta(minutes=45)).time()
        super().save(*args, **kwargs)


