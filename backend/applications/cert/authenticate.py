import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.exceptions import AuthenticationFailed


def token_invalidation(refresh_token):
    # 토큰 무효화
    refresh_token_str = str(refresh_token)
    decoded_token = jwt.decode(refresh_token_str, options={"verify_signature": False})  # 서명 검증 없이 디코드
    jti = decoded_token.get('jti')

    if jti:
        outstanding_token = OutstandingToken.objects.filter(jti=jti).first()
        if outstanding_token:
            BlacklistedToken.objects.get_or_create(token=outstanding_token)
            return True
    return False
