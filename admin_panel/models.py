from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Access(models.TextChoices):
    superuser = 'superuser', 'سوپر ادمین'
    admin = 'admin', 'ادمین عادی'


class AdminPanel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('user'))
    access = models.CharField(choices=Access.choices, default=Access.admin, max_length=15, verbose_name=_('access'))


    
    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name_plural = _('admins panel')
        verbose_name = _('admin panel')
