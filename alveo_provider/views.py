'''
Created on 10 Feb 2017

@author: Michael
'''
import requests

from allauth.socialaccount.providers.oauth2.views import (OAuth2Adapter,
                                                          OAuth2LoginView,
                                                          OAuth2CallbackView)
import pyalveo
from .provider import AlveoProvider


class AlveoOAuth2Adapter(OAuth2Adapter):
    provider_id = AlveoProvider.id
    access_token_url = 'https://alveo-staging.sol1.net/oauth/token'
    authorize_url = 'https://alveo-staging.sol1.net/oauth/authorize'
    profile_url = 'https://alveo-staging.sol1.net/oauth2/v1/userinfo'

    def complete_login(self, request, app, token, **kwargs):
        resp = requests.get(self.profile_url,
                            params={'access_token': token.token,
                                    'alt': 'json'})
        resp.raise_for_status()
        extra_data = resp.json()
        login = self.get_provider() \
            .sociallogin_from_response(request,
                                       extra_data)
        return login


oauth2_login = OAuth2LoginView.adapter_view(AlveoOAuth2Adapter)
oauth2_callback = OAuth2CallbackView.adapter_view(AlveoOAuth2Adapter)