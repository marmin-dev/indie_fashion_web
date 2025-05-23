from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from applications.cert.models import IndieUser


class RegisterSerializer(serializers.ModelSerializer):
    # 회원 가입 시리얼 라이저
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = IndieUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = IndieUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    # 회원 탈퇴
    def withdraw(self, validated_data):
        user = IndieUser.objects.delete_user(email=validated_data)
        return user

    # 유저 정보 시리얼라이저
    class Meta:
        model = IndieUser
        fields = ['username', 'email']


class ChangePasswordSerializer(serializers.Serializer):
    # 비밀번호 변경 시리얼라이저
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        user = self.context['request'].user
        if not user.check_password(attrs['old_password']):
            raise serializers.ValidationError({"old_password": "현재 비밀번호가 일치하지 않습니다."})
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
