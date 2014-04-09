from django.db import models
from django.contrib.auth.models import User, Group

# Custom Registration Fields to gather more information about the user.
from registration.supplements import RegistrationSupplementBase


from registration.backends import get_backend
from registration.signals import user_activated


class RegistrationCustomFields(RegistrationSupplementBase):

    institution = models.CharField("Institution Name", max_length=100)
    full_name = models.CharField("Full Name", max_length=100)
    

    def __unicode__(self):
        # a summary of this supplement
        return "%s (%s)" % (self.institution, self.full_name)


def assign_user_to_group(sender, user, password, is_generated, request, **kwargs):
  backend = get_backend()
  g = Group.objects.get(name='research')
  g.user_set.add(user)


  #backend.accept(profile, request=request)
user_activated.connect(assign_user_to_group)
