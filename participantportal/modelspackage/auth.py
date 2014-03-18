from django.contrib.auth.models import User, Group
from django.db import transaction
from browse.modelspackage.participants import *
from participantportal.helpers import read_model_property
from participantportal.models import UserProfile


class CustomAuthBackend(object):
  """ This custom authenticator is plugged into authentication pipeline
  and is configured in settings.py."""
  def authenticate(self, colour, animal, birth_year = None, gender = None):
    #print "Custom Authenticator Invoked with params %s-%s-%s-%s" % (colour, animal, birth_year, gender)
    username = "%s_%s" % (colour, animal)
    participant = Participant.objects.get(username)

    if not participant is None:
      # Before creating the user check to make sure the
      # gender and birth year match
      if birth_year == read_model_property(participant, 'birthYear') and gender == read_model_property(participant, 'gender'):
        try:
          user = User.objects.get(username = username)
        except User.DoesNotExist:
          user = self.create_user(username)

        return user

    return None

  @transaction.commit_on_success  
  def create_user(self, username):
    user = User(username = username, is_staff = False, is_active = True, is_superuser = False)
    user.set_unusable_password()
    user.save()

    self.add_user_to_participant_group(user)

    up = UserProfile.objects.create(user = user)
    up.save()
    up.initialise_agreement()
    return user


  def add_user_to_participant_group(self, user):
    participant_group = Group.objects.get(name = 'participants')
    user.groups.add(participant_group)


  def get_user(self, user_id):
    try:
      return User.objects.get(pk = user_id)
    except User.DoesNotExist:
      return None