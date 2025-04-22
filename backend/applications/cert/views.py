from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


class CertViewSet(GenericViewSet):

    @action(detail=False, methods=['POST'])
    def login(self, request):
        pass

    @action(detail=False, methods=['GET'])
    def logout(self):
        pass

    @action(detail=False, methods=['GET'])
    def get_user_info(self):
        pass

    @action(detail=False, methods=['POST'])
    def change_pw(self):
        pass

    @action(detail=False, methods=['POST'])
    def sign_up(self):
        pass

