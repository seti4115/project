from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from user.validators import phone_validator, persian_validator

User = get_user_model()


class Type(models.TextChoices):
    CONSULTING = 'consulting', 'مشاوره'
    SPRAYING = 'spraying', 'سم پاشی'


class Status(models.TextChoices):
    PENDING = 'pending', 'در انتظار بررسی'
    APPROVED = 'approved', 'تایید شده'
    REJECTED = 'rejected', 'رد شده'


class Request(models.Model):
    type = models.CharField(
        choices=Type.choices,
        max_length=10,
        verbose_name=_('نوع درخواست'),
        blank=True,
        db_index=True
    )
    first_name = models.CharField(_('نام'), max_length=25, validators=[persian_validator])
    last_name = models.CharField(_('نام خانوادگی'), max_length=40, validators=[persian_validator])
    phone = models.CharField(_('تلفن'), validators=[phone_validator], max_length=12, db_index=True)  # ✅ index روی شماره
    province = models.CharField(max_length=150, verbose_name=_('استان'))
    city = models.CharField(max_length=150, verbose_name=_('شهر'))
    land_product = models.CharField(max_length=200, verbose_name=_('محصول زمین'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('ایجاد شده در'), db_index=True)  # ✅ index روی تاریخ
    status = models.CharField(
        _('وضعیت'),
        choices=Status.choices,
        default=Status.PENDING,
        max_length=10,
        db_index=True
    )

    def __str__(self):
        return f'{self.id} - {self.phone} - {self.type}'

    class Meta:
        verbose_name = _('درخواست')
        verbose_name_plural = _('درخواست‌ها')
        ordering = ['-created_at']

        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['status']),
            models.Index(fields=['type']),
            models.Index(fields=['created_at']),
            models.Index(fields=['phone', 'status']),
            models.Index(fields=['type', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]

        abstract = True


class ConsultingRequest(Request):
    message = models.TextField(_('توضیحات'))
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name=_('کاربر'),
        null=True,
        blank=True,
        related_name='requests_consulting'
    )

    def save(self, *args, **kwargs):
        self.type = Type.CONSULTING
        if self.user:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('درخواست مشاوره')
        verbose_name_plural = _('درخواست‌های مشاوره')
        indexes = [
            models.Index(fields=['phone'], name='consulting_phone'),
            models.Index(fields=['status'], name='consulting_status'),
            models.Index(fields=['created_at'], name='consulting_created'),
        ]


class SprayingRequest(Request):
    land_area = models.PositiveIntegerField(verbose_name=_('مساحت زمین (عدد به هکتار)'))
    address = models.TextField(verbose_name=_('آدرس زمین'))
    message = models.TextField(blank=True, verbose_name=_('توضیحات تکمیلی'), null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name=_('کاربر'),
        null=True,
        blank=True,
        related_name='requests_spraying'
    )

    def save(self, *args, **kwargs):
        self.type = Type.SPRAYING
        if self.user:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('درخواست سم‌پاشی')
        verbose_name_plural = _('درخواست‌های سم‌پاشی')
        indexes = [
            models.Index(fields=['phone'], name='spraying_phone'),
            models.Index(fields=['status'], name='spraying_status'),
            models.Index(fields=['created_at'], name='spraying_created'),
        ]
