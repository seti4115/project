from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.crypto import get_random_string

from django.utils.translation import gettext as _


class User(AbstractUser):
    persian_validator = RegexValidator(
        regex=r'^[\u0600-\u06FF\s\u200c]+$',
        message="فقط حروف فارسی مجاز است."
    )
    first_name = models.CharField(_('first name'), max_length=20, validators=[persian_validator, ])
    last_name = models.CharField(_('last name'), max_length=20, validators=[persian_validator, ])

    username = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="نام کاربری",
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9@._\-*]+$',
                message="فقط حروف، اعداد و نمادهای @ . _ - * مجاز هستند."
            )
        ]
    )
    phone_regex = RegexValidator(
        regex=r"^989\d{2}\s*?\d{3}\s*?\d{4}$", message=_("Invalid phone number."),
    )
    phone = models.CharField(
        max_length=12, validators=[phone_regex],
        unique=True, verbose_name=_("phone"), db_index=True
    )
    email = models.EmailField(_('email address'), unique=True, blank=True, null=True)

    activation_code = models.CharField(max_length=128, editable=False, null=True)

    def save(self, *args, **kwargs):
        if self.activation_code is None:
            self.activation_code = get_random_string(128)

        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username
