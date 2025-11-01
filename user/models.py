from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.utils.translation import gettext as _
from rest_framework.reverse import reverse

from user.validators import phone_validator, persian_validator, english_validator


class UserBase(AbstractUser):
    first_name = models.CharField(_('نام'), max_length=25, validators=[persian_validator, ])
    last_name = models.CharField(_('نام خانوادگی'), max_length=40, validators=[persian_validator, ])
    username = models.CharField(_('نام کاربری'), max_length=30, unique=True, validators=[english_validator])
    phone = models.CharField(_("شماره تلفن"), max_length=12, validators=[phone_validator], unique=True, db_index=True)
    email = models.EmailField(_('آدرس ایمیل'), blank=True, null=True)
    activation_code = models.CharField(_('کد فعالسازی'), max_length=128, editable=False)
    is_admin = models.BooleanField(default=False, verbose_name=_('ادمین'))

    def save(self, *args, **kwargs):
        if self.activation_code is None:
            self.activation_code = get_random_string(128)
            print(self.activation_code)
        return super(UserBase, self).save(*args, **kwargs)

    def __str__(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return self.username

    def get_absolute_url(self):
        return reverse('user-list-detail', kwargs={'phone': self.phone})

    class Meta:
        abstract = True
        unique_together = ('phone', 'activation_code')


class User(UserBase):
    class Meta:
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')
        ordering = ['-date_joined', '-phone']
        indexes = [
            models.Index(fields=['phone'], condition=Q(is_active=True), name='phone'),
            models.Index(fields=['username'], condition=Q(is_active=True), name='username'),
        ]
