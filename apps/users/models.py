from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def _create_user(self, mobile, password, **extra_fields):
        if not mobile:
            raise ValueError('The given mobile must be set')
        user = self.model(mobile=mobile ,**extra_fields)
        user.set_password(password)
        user.save()
        return user


    def create_user(self, mobile, password=None, **extra_fields):
        if not mobile:
            raise ValueError('The given mobile must be set')
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        return self._create_user(mobile, password, **extra_fields)


    def create_superuser(self, mobile, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        return self._create_user(mobile, password, **extra_fields)




class User(AbstractBaseUser, PermissionsMixin):
    mobile = models.CharField(max_length=20, unique=True)
    email = models.CharField(blank =True , null = True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    description = models.TextField(blank=True , null= True)
    birth_date = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profiles/",blank=True, null=True)
    is_active =models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True , null=True)

    USERNAME_FIELD ="mobile"
    REQUIRED_FIELDS = []

    objects = UserManager()

    @property
    def full_name(self):
        if not self.first_name and  not self.last_name:
            return self.mobile
        else :
            return f"{self.first_name} {self.last_name}".strip()
    def __str__(self):
        return self.full_name
