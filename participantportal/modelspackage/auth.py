from django.contrib.auth.models import User
from browse.modelspackage.participants import *
from participantportal.helpers import read_model_property

class CustomAuthBackend(object):
  """ This custom authenticator is plugged into authentication pipeline
  and is configured in settings.py."""

  def authenticate(self, colour, animal, birth_year = None, gender = None):
    # Check to see if the user can be found in the repository, and if so 
    # generate a username and store it locally for future authentication
    # print "Custom Authenticator Invoked with params %s-%s-%s-%s" % (colour, animal, birth_year, gender)
    username = "%s_%s" % (colour, animal)
    participant = Participant.objects.get(username)

    if not participant is None:
      # Before creating the user check to make sure the
      # gender and birth year match
      if birth_year == read_model_property(participant, 'birthYear') and \
          gender == read_model_property(participant, 'gender'):
        try:
          user = User.objects.get(username = username)
        except User.DoesNotExist:
          user = User(username = username, is_staff = True, is_active = True, is_superuser = False)
          user.set_unusable_password()
          user.save()
        return user

    return None

  def get_user(self, user_id):
    try:
      return User.objects.get(pk = user_id)
    except User.DoesNotExist:
      return None