from django.contrib.auth.models import Permission, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import UserBase


class Access(models.TextChoices):
    superuser = 'superuser', 'superuser'
    admin = 'admin', 'admin'


class AdminPanel(UserBase):
    access = models.CharField(choices=Access.choices, default=Access.admin, max_length=15)
    groups = models.ManyToManyField(
        Group,
        related_name='adminpanel_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='adminpanel_permission_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    class Meta:
        verbose_name_plural = _('admins panel')
        verbose_name = _('admin panel')
