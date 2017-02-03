from django.db import models
from django.contrib.auth.models import User, Group


from registration.supplements.base import RegistrationSupplementBase


from registration.backends import get_backend
from registration.signals import user_activated

# Custom Registration Fields to gather more information about the user.
class RegistrationCustomFields(RegistrationSupplementBase):

    institution = models.CharField("Institution Name", max_length=100)
    full_name = models.CharField("Full Name", max_length=100)
    

    def __unicode__(self):
        # a summary of this supplement
        return "%s (%s)" % (self.institution, self.full_name)

# Automatically assign a user to research group when the account is activated
# Done through user_activated signal
def assign_user_to_group(sender, user, password, is_generated, request, **kwargs):
  backend = get_backend()
  g = Group.objects.get(name='research')
  g.user_set.add(user)

user_activated.connect(assign_user_to_group)
