from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def otp_verified_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        # JWT payload에서 otp_verified 가져오기
        otp_verified = False
        if hasattr(request, 'auth') and hasattr(request.auth, 'payload'):
            otp_verified = request.auth.payload.get('otp_verified', False)

        if not otp_verified:
            return Response({'detail': 'OTP 인증이 필요합니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        return view_func(self, request, *args, **kwargs)

    return _wrapped_view
