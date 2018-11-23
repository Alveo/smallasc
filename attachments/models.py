from django.db import models
from django.contrib.auth import models as authmodels
from django.conf import settings
from django.dispatch import receiver

import os

# Models for file attachments uploaded to the site
# basically just a simple container for files
# but allowing for replacement of previously uploaded files
class Attachment(models.Model):

    file = models.FileField(upload_to=settings.ATTACHMENT_LOCATION)
    description = models.TextField(blank=True)
    date = models.DateField(auto_now=True)
    uploader = models.ForeignKey(authmodels.User)

@receiver(models.signals.post_delete, sender=Attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Attachment` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
    return True