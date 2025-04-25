from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from applications.common.base_model import TimeStampModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class IndieUser(AbstractBaseUser, TimeStampModel):
    # 사용자
    objects = UserManager()
    email = models.EmailField(max_length=254, unique=True)
    is_active = models.BooleanField(default=True)
    username = models.CharField(max_length=255, null=False, blank=False)
    last_login = models.DateTimeField(auto_now=True)
    fail_cnt = models.IntegerField(default=0)
    # 1 = 관리자, 2 = 사용자
    policy_id = models.IntegerField(null=False, blank=False, default=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def change_password(self, user, password):
        self.password = password
        self.save()

