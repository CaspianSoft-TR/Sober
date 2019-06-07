import datetime
from rest_framework_jwt.settings import api_settings

from api.serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    """ Custom response payload handler.

    This function controlls the custom payload after login or token refresh. This data is returned through the web API.
    """
    return {
        'access_token': token,
        'token_type': 'Bearer',
        'expired_at': datetime.datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA,
        'user': UserSerializer(user, context={'request': request}).data
    }
