from browse.modelspackage.participants import *
from browse.modelspackage.sites import *
from django.test import TestCase
from participantportal.modelspackage.auth import CustomAuthBackend
from participantportal.helpers import *

class AuthenticationTests(TestCase):
    
  def test_authenitcation_for_valid_user(self):
    auth_backend = CustomAuthBackend()
    user = auth_backend.authenticate('1', '1093', '1984', 'female')
    self.assertIsNotNone(user)

  def test_authentication_for_invalid_user(self):
    auth_backend = CustomAuthBackend()
    user = auth_backend.authenticate('1', '62')
    self.assertIsNone(user)

  def test_retrieve_participant_data(self):
    participant = Participant.objects.get('1_1093')
    self.assertIsNotNone(participant)
    # print participant.properties()

  def test_retrieve_site(self):
    site_id = get_site_id_from_url('http://id.austalk.edu.au/protocol/site/UTAS')
    site = Site.objects.get(site_id)
    self.assertIsNotNone(site)