from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet


class CertViewSet(GenericViewSet):

    @action(detail=False, methods=['POST'])
    def login(self, request):
        pass

    def logout(self):
        pass

    def get_user_info(self):
        pass

    def change_pw(self):
        pass

    def signup(self):
        pass

