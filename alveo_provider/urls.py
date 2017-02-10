'''
Created on 10 Feb 2017

@author: Michael
'''
from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from provider import AlveoProvider

urlpatterns = default_urlpatterns(AlveoProvider)