from django.db import models

class Animal (models.Model):
    """ Each participant is de-identified using a colour and animal, this class represents
    the animal. """
    
    # Note that id is not specified as this is a Django model
    name = models.CharField (max_length = 255)

    class Meta:
        app_label = 'baseapp'