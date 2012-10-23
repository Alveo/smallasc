from django.utils import unittest
from baseapp.models import Colour

class LookupTests (unittest.TestCase):

    def test_create_simple_colour (self):
        colour = Colour.objects.create (name = "Purple")
