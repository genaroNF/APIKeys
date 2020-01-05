
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.hashers import check_password

from .models import APIKey, APIKey2
import logging
import base64
import json

from rest_framework import HTTP_HEADER_ENCODING

logger = logging.getLogger('django')

class ApiKeyAuthentication(TokenAuthentication):

    model = None
    header = None
    header_text = ''
    base64_encoded = False
    start_index = 0 

    def get_token_from_auth_header(self, auth):
        auth = auth.split()
        if not auth or auth[0].lower() != self.header_text.encode('utf-8'):
            return None

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            if self.base64_encoded:
                return base64.b64decode(auth[1].decode()).decode()[self.start_index:]
            else:
                return auth[1].decode()[self.start_index:]
        except UnicodeError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

    def authenticate(self, request):
        auth = get_authorization_header(request)
        if self.header is not None and auth is b'':
            auth = request.META.get(self.header, '').encode(HTTP_HEADER_ENCODING)
        token = self.get_token_from_auth_header(auth)
        
        if token:
            return self.authenticate_credentials(token)
        return None

    def authenticate_credentials(self, key):
        logger.info(key)
        try:
            prefix, key_unhashed = key.split('.')
            token = self.model.objects.get(prefix=prefix)
        except (self.model.DoesNotExist, ValueError):
            raise AuthenticationFailed('Invalid Api key.')

        if not check_password(key_unhashed, token.key):
            raise AuthenticationFailed('Invalid Api key.')

        if not token.is_active:
            raise AuthenticationFailed('Api key inactive or deleted.')
        
        if hasattr(token, 'user'):
            user = token.user # what ever you want here
            return (user, token)
        else:
            return  (None, token)

class ApiKey2Authentication(ApiKeyAuthentication):

    model = APIKey2
    header_text = 'api-key'
    header = 'HTTP_API_KEY'

class BasicHTTPApiKeyAuthentication(ApiKeyAuthentication):

    model = APIKey2
    header_text = 'basic'
    base64_encoded = True
    start_index = 1