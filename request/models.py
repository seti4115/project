from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from user.validators import phone_validator

User = get_user_model()


class Type(models.TextChoices):
    CONSULTING = 'consulting', 'مشاوره'
    SALE = 'sale', 'فروش'
    SPRAYING = 'spraying', 'سم پاشی'


class Status(models.TextChoices):
    PENDING = 'pending', 'در انتظار بررسی'
    APPROVED = 'approved', 'تایید شده'
    REJECTED = 'rejected', 'رد شده'


class Request(models.Model):
    type = models.CharField(choices=Type.choices, max_length=10, verbose_name=_('نوع درخواست'))
    user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name=_('کاربر'), null=True, blank=True,
                             related_name='requests')
    phone = models.CharField(_('شماره تلفن'), validators=[phone_validator, ], max_length=12)
    message = models.TextField(verbose_name=_('پیغام'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('ایجاد شده در'))
    status = models.CharField(_('وضعیت'), choices=Status.choices, default=Status.PENDING, max_length=10)

    def __str__(self):
        return f'{self.id} - {self.phone} - {self.type}'

    class Meta:
        verbose_name = _('درخواست')
        verbose_name_plural = _('درخواست ها')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone'])
        ]
