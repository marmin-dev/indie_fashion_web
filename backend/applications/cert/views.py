from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from applications.cert.serializers import RegisterSerializer, UserSerializer, ChangePasswordSerializer
from applications.common.http_response_collections import NOT_AUTHORIZED


class CertViewSet(ViewSet):

    @action(detail=False, methods=['POST'])
    def login(self, request):
        # 로그인
        username = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token),'refresh': str(refresh)})
        else:
            return NOT_AUTHORIZED

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
        return Response(
            {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            },
            status=status.HTTP_200_OK
        )




