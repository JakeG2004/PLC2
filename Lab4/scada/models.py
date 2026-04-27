from django.db import models

class LogEntry(models.Model):
    date = models.DateTimeField()
    value1 = models.IntegerField()
    value2 = models.IntegerField()