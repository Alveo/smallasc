from django.test import TestCase
from participantportal.modelspackage.auth import CustomAuthBackend

class AuthenticationTests(TestCase):
    
  def test_authenitcation_for_valid_user(self):
    auth_backend = CustomAuthBackend()
    user = auth_backend.authenticate(1, 1093)
    self.assertIsNotNone(user)

  def test_authentication_for_invalid_user(self):
    auth_backend = CustomAuthBackend()
    user = auth_backend.get_user('1_62')
    self.assertIsNone(user)