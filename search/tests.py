from django.utils import unittest
from search.models.sites import Sites

class SiteTests (unittest.TestCase):

	def setUp (self):
		self.site1 = Sites.objects.create (name = "Australian National University", location = "Canberra")


	def test_site_prettyprinted_name (self):
		self.assertEqual ("Australian National University, Canberra", str (self.site1))