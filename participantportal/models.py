from baseapp.modelspackage.animals import Animal
from baseapp.modelspackage.colours import Colour
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField

class UserProfile(models.Model):
  # This field is required.
  user = models.OneToOneField(User,on_delete=models.CASCADE)

  def __unicode__(self):
      return self.colour() + " " + self.animal()
      
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
  
  #legalise = models.TextField()
  legalise = HTMLField()

  def __unicode__(self):
    return u'%s' % (self.legalise[:20])


class AgreementStatus(models.Model):
  
  agreement       = models.ForeignKey(Agreement,on_delete=models.CASCADE)
  user            = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
  has_agreed      = models.BooleanField(default = False)
  agreement_date  = models.DateField(null = True)

  def accept(self, accepted_on):
    self.has_agreed = True
    self.agreement_date = accepted_on
    
    
  def __unicode__(self):
      if self.has_agreed: 
          what = " - yes"
      else:
          what = " - no"
      return str(self.user) + " - " + str(self.agreement) + what
