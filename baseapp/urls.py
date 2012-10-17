from django.conf.urls import patterns, include, url
from baseapp.views.security import logout

urlpatterns = patterns('baseapp.views',
    # Security related pages
    (r'^logout/$', logout),
)
