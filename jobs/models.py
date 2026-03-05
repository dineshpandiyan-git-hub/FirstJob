from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_recruiter = models.BooleanField(default=False)


class Job(models.Model):
    recruiter = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.TextField()

    def __str__(self):
        return self.title


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    match_score = models.FloatField()
    status = models.CharField(max_length=20, default="Submitted")