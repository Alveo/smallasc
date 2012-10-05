from django.contrib import admin
from search.modelspackage.sites import Site

# Register the sites we would like to appear in the administration application
admin.site.register(Site)