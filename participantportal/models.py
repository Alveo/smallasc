from baseapp.modelspackage.animals import Animal
from baseapp.modelspackage.colours import Colour
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  # This field is required.
  user = models.OneToOneField(User)


  def colour(self):
    colour_id = self.user.username.split('_')[0]
    return Colour.objects.get(id = colour_id).name

  def animal(self):
    animal_id = self.user.username.split('_')[1]
    return Animal.objects.get(id = animal_id).name

  def initialise_agreement(self):
    """ This function initialises the agreement for the participant """
    agreements = Agreement.objects.all()
    for agreement in agreements:
      agreement_status = AgreementStatus(agreement = agreement, user = self, has_agreed = False)
      agreement_status.save()

  def has_accepted_agreements(self):
    for agreement in self.agreementstatus_set.all():
      if agreement.has_agreed == False:
        return False

    return True


class Agreement(models.Model):
  
  legalise = models.TextField()

  def __unicode__(self):
    return u'%s' % (self.legalise)


class AgreementStatus(models.Model):
  
  agreement       = models.ForeignKey(Agreement)
  user            = models.ForeignKey(UserProfile)
  has_agreed      = models.BooleanField(default = False)
  agreement_date  = models.DateField(null = True)

  def accept(self, accepted_on):
    self.has_agreed = True
    self.agreement_date = accepted_on


# Custom Registration Fields to gather more information about the user.
from registration.supplements import RegistrationSupplementBase
class RegistrationCustomFields(RegistrationSupplementBase):

    institution = models.CharField("Institution Name", max_length=100)
    full_name = models.CharField("Full Name", max_length=100)
    

    def __unicode__(self):
        # a summary of this supplement
        return "%s (%s)" % (self.institution, self.full_name)