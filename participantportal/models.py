from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  # This field is required.
  user            = models.OneToOneField(User)

  def initialise_agreement(self):
    """ This function initialises the agreement for the participant """
    agreements = Agreement.objects.all()
    for agreement in agreements:
      agreement_status = AgreementStatus(agreement = agreement, user = self, has_agreed = False)
      agreement_status.save()

class Agreement(models.Model):
  legalise        = models.TextField()

  def __unicode__(self):
    return u'%s' % (self.legalise)

class AgreementStatus(models.Model):
  agreement       = models.ForeignKey(Agreement)
  user            = models.ForeignKey(UserProfile)
  has_agreed      = models.BooleanField(default = False)
  agreement_date  = models.DateField(null = True)