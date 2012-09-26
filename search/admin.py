from django.contrib import admin
from search.models.sites import Sites

# Register the sites we would like to appear in the administration application
admin.site.register(Sites)