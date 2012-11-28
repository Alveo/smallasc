from django.db import models

class Animal (models.Model):
    """ Each participant is de-identified using a colour and animal, this class represents
    the animal. """
    name = models.CharField (max_length = 255)

    def __unicode__(self):
      return u'%s' % (self.name)

    class Meta:
        app_label = 'baseapp'