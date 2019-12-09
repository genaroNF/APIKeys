
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from django.contrib.auth.hashers import check_password

from .models import APIKey, APIKey2
import logging
import base64

logger = logging.getLogger('django')


class ApiKeyAuthentication(TokenAuthentication):

    model = APIKey2

    def get_token_from_auth_header(self, auth):
        auth = auth.split()
        if not auth or auth[0].lower() != b'api-key':
            return None

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            return auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

    def authenticate(self, request):
        auth = get_authorization_header(request)
        token = self.get_token_from_auth_header(auth)

        if not token:
            token = request.GET.get('api-key', request.POST.get('api-key', None))

        if token:
            return self.authenticate_credentials(token)
        return None

    def authenticate_credentials(self, key):
        logger.info(key)
        logger.info(123)
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

    def authenticate_header(self, request):
        return 'apì-key'

class BasicHTTPApiKeyAuthentication(TokenAuthentication):

    model = APIKey2

    def get_token_from_auth_header(self, auth):
        auth = auth.split()
        if not auth or auth[0].lower() != b'basic':
            return None

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            return base64.b64decode(auth[1].decode()).decode()
        except Exception:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

    def authenticate(self, request):
        auth = get_authorization_header(request)
        token = self.get_token_from_auth_header(auth)

        if token:
            return self.authenticate_credentials(token)
        return None

    def authenticate_credentials(self, key):
        logger.info(key[1:])
        logger.info('asdasdassdas')
        try:
            prefix, key_unhashed = key[1:].split('.')
            token = self.model.objects.get(prefix=prefix)
        except (self.model.DoesNotExist, ValueError) as e:
            logger.info(e)
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

    def authenticate_header(self, request):
        return 'basic'

