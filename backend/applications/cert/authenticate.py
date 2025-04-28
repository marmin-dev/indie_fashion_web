import jwt
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


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


class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # 인증 토큰을 가져옴
        raw_token = self.get_raw_token(request)

        # 토큰이 블랙리스트에 있는지 확인
        if BlacklistedToken.objects.filter(token=raw_token).exists():
            from rest_framework_simplejwt.exceptions import AuthenticationFailed
            raise AuthenticationFailed('이미 만료된 토큰 입니다')

        # 기본 JWT 인증 로직
        return super().authenticate(request)