from django.db import models

class User(models.Model):
    nr_matricol = models.CharField(max_length=64)

class Timetable(models.Model):
    username = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    datetime = models.DateTimeField()