from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid
from django.db.models import signals
from django.core.exceptions import ValidationError


class UserAccountManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address must be provided')

        if not password:
            password = None
            # raise ValueError('Password must be provided')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        print(extra_fields)
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    REQUIRED_FIELDS = ['email', 'full_name']
    USERNAME_FIELD = 'nickname'

    objects = UserAccountManager()

    nickname = models.CharField('nickname', unique=True, blank=False, null=False, max_length=200)
    email = models.EmailField('email', unique=True, blank=False, null=False)
    full_name = models.CharField('full name', blank=False, null=True, max_length=400)
    is_staff = models.BooleanField('staff status', default=False)
    is_superuser = models.BooleanField('superuser status', default=False)
    is_active = models.BooleanField('active', default=True)
    restore_password_uuid = models.UUIDField(default=None, blank=True, null=True)
    is_manager = models.BooleanField(default=True)
    is_seller = models.BooleanField(default=False)

    def get_short_name(self):
        return self.email

    @property
    def display_name(self):
        if not self.full_name:
            return self.nickname
        else:
            return self.full_name

    def __unicode__(self):
        return self.email


from django.contrib.auth.backends import ModelBackend

class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'nickname': username}
        try:
            user = User.objects.get(**kwargs)
            if user.check_password(password):
                return user
            else:
                raise ValidationError("wrong password")
        except User.DoesNotExist:
            raise User.DoesNotExist

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


