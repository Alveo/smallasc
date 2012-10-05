from django.contrib import admin
from baseapp.models import Animal, Colour

# Register the sites we would like to appear in the administration application
admin.site.register (Animal)
admin.site.register (Colour)