from rest_framework import serializers

from applications.cert.models import IndieUser


class RegisterSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = IndieUser
        fields = ['username', 'email']

