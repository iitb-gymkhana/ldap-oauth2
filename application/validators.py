from datetime import timedelta

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from oauth2_provider.models import get_application_model as get_oauth2_application_model
from oauth2_provider.models import AccessToken, RefreshToken
from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.settings import oauth2_settings

from core.utils import get_default_scopes


class CustomOAuth2Validator(OAuth2Validator):

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        application = get_object_or_404(get_oauth2_application_model(), client_id=client_id)
        return get_default_scopes(application)

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        request.scopes = list(set(request.scopes).union(set(get_default_scopes(client))))
        return super(CustomOAuth2Validator, self).validate_scopes(client_id, scopes, client, request, *args, **kwargs)

