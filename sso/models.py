from django.db import models
from django.contrib.auth.models import User


class TSession(models.Model):
        user = models.ForeignKey(User, db_index=True,on_delete=models.CASCADE)
        tsession_key = models.CharField(max_length=64, db_index=True)
        session_key = models.CharField(max_length=40)
        expire_date = models.DateTimeField(db_index=True)

