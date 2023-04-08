from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, first_name, last_name, mobile, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, first_name, last_name, mobile, password, **other_fields)

    def create_user(self, email, first_name, last_name, mobile, password, **other_fields):

        if not email:
            raise ValueError(_('You must provide an email address'))
        if not first_name:
            raise ValueError(_('You must provide an first_name address'))
        if not last_name:
            raise ValueError(_('You must provide an last_name address'))
        if not mobile:
            raise ValueError(_('You must provide an mobile address'))
        if not password:
            raise ValueError(_('You must provide an password address'))

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, mobile=mobile, 
                          **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    GENDERS = (
        (1, "Male"),
        (2, "Female"),
        (3, "Other")
    )

    gender = models.CharField(_("Gender"),max_length=1, choices=GENDERS ,null=True, blank=True)
    first_name = models.CharField(_("First Name"),max_length=50, blank=True, null=True)
    last_name = models.CharField(_("Last Name"),max_length=100)
    email = models.EmailField(_('email address'), unique=True)
    mobile = models.CharField(_("Mobile"),max_length=20)
    
    # Settings tab
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', "last_name", "mobile"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"