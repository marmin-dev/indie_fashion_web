from io import BytesIO

import base64
import pyotp
import qrcode
from django.contrib.auth import authenticate
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponse
from applications.cert.authenticate import token_invalidation
from applications.cert.decorators import otp_verified_required
from applications.cert.serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer


class CertViewSet(ViewSet):
    @action(detail=False, methods=['POST'])
    def login(self, request):
        # 이메일과 비밀번호로 사용자 인증
        email = request.data.get('email')
        password = request.data.get('password')
        otp_token = request.data.get('otp_token')  # OTP 토큰 받기

        # 사용자 인증
        user = authenticate(username=email, password=password)

        if user is None:
            return Response({'detail': '잘못된 이메일 또는 비밀번호입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
        is_otp = False
        # OTP 인증 추가
        if otp_token:
            # 사용자에게 연결된 TOTP 디바이스가 있는지 확인
            try:
                device = TOTPDevice.objects.get(user=user)

            except TOTPDevice.DoesNotExist:
                return Response({'detail': '사용자의 OTP 디바이스가 설정되지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

            # OTP 검증
            if not device.verify_token(otp_token):
                return Response({'detail': 'OTP가 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
            is_otp = True
        else:
            try:
                device = TOTPDevice.objects.get(user=user)
                if device:
                    return Response({'detail': 'OTP가 유효하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)
            except TOTPDevice.DoesNotExist:
                pass

        # OTP가 성공적으로 인증되었으면 JWT 토큰 생성
        refresh = RefreshToken.for_user(user)
        if is_otp:
            refresh['otp_verified'] = True
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        })

    @action(detail=False, methods=['POST'])
    def register(self, request):
        # 회원 가입
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Success',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def get_totp_qrcode(self, request):
        user = request.user  # 이미 인증된 사용자 정보는 request.user에서 가져올 수 있습니다.

        # 사용자가 TOTP 디바이스를 설정했는지 확인하고, 없다면 새로 생성
        try:
            device = TOTPDevice.objects.get(user=user)
        except TOTPDevice.DoesNotExist:
            device = user.create_totp_device()

        # bin_key를 base32로 인코딩하여 secret으로 사용
        secret = base64.b32encode(device.bin_key).decode('utf-8')  # base32로 인코딩 후 UTF-8 디코딩
        totp = pyotp.TOTP(secret)
        uri = totp.provisioning_uri(name=user.email, issuer_name="DemoBackend")  # QR 코드 URI 생성
        img = qrcode.make(uri)

        # 이미지 IO로 변환
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)  # 이미지의 처음부터 읽을 수 있도록 이동

        return HttpResponse(img_io, content_type='image/png')

    @otp_verified_required
    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def info(self, request):
        # 내 정보 불러오기
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)


    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def change_pw(self, request):
        # 비밀번호 변경
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        BlacklistedToken.objects.get_or_create(token=refresh)
        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def withdraw(self, request):
        # 회원 탈퇴
        user = request.user
        serializer = UserSerializer(user)
        serializer.withdraw(user)
        return Response({"message":"Successfully Deleted"},status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        # 로그아웃(토큰 무효화)
        user = request.user
        refresh_token = RefreshToken.for_user(user)
        if token_invalidation(refresh_token=refresh_token):
            return Response({"message": "Successfully Logout"}, status=status.HTTP_200_OK)
        return Response({"message":"Logout Failed"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


