from django.db import models

# Create your models here.

class Files2taskId(models.Model):
    h = models.CharField(max_length=128)
    task_id = models.CharField(max_length=128)
    dt = models.DateTimeField(auto_now_add=True)

