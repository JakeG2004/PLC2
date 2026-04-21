from django.db import models

class LogEntry(models.Model):
    date = models.DateTimeField()
    log_type = models.CharField(max_length=32)
    message = models.CharField(max_length=256)

class SldEntry(models.Model):
    date = models.DateTimeField()
    value = models.IntegerField()