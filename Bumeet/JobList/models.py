from django.db import models

# Create your models here.

class Job(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
    company = models.CharField(max_length=100, null=False, blank=False)
    location = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=500, null=False, blank=False)
    ended_date = models.DateField(null=True, blank=True)