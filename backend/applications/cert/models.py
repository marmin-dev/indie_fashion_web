from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from applications.common.base_model import TimeStampModel


class UserManager(BaseUserManager):
    use_in_migrations = True


class IndieUser(AbstractBaseUser, TimeStampModel):
    objects = UserManager()
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    last_login = models.DateTimeField(auto_now=True)

