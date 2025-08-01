from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _

from user.validators import phone_validator, persian_validator, english_validator


class UserBase(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=25, validators=[persian_validator, ])
    last_name = models.CharField(_('last name'), max_length=40, validators=[persian_validator, ])
    username = models.CharField(_('username'), max_length=30, unique=True, validators=[english_validator])
    phone = models.CharField(_("phone number"), max_length=12, validators=[phone_validator], unique=True, db_index=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    activation_code = models.CharField(_('activation code'), max_length=128, editable=False, null=True)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.activation_code is None:
            self.activation_code = get_random_string(128)

        return super(UserBase, self).save(*args, **kwargs)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

    class Meta:
        abstract = True


class User(UserBase):
    pass
