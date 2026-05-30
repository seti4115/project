from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse
from taggit.managers import TaggableManager
from translate import Translator

from user.validators import persian_validator, english_validator

translator = Translator(to_lang="en")


class Type(models.TextChoices):
    FERTILIZER = 'Fertilizer', 'کود'
    POISON = 'Poison', 'سم'
    COMBINED = 'Combined', 'ترکیبی'


class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name=_('نام'), validators=[persian_validator])
    title_en = models.CharField(max_length=100, blank=True, verbose_name=_('نام انگلیسی'), validators=[english_validator], null=True)
    slug = models.SlugField(max_length=100, blank=True, unique=True, verbose_name=_('اسلاگ'), null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('وزن'))
    type = models.CharField(max_length=10, choices=Type.choices, verbose_name=_('نوع'))
    brand = models.CharField(max_length=50, verbose_name=_('برند'))
    description = models.TextField(verbose_name=_('توضیحات'))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('قیمت'))
    production_date = models.DateField(verbose_name=_('تاریخ تولید'))
    expiration_date = models.DateField(verbose_name=_('تاریخ انقضا'))
    tags = TaggableManager(verbose_name=_('تگ ها'), blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('فعال بودن'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('ویرایش شده در'))

    def __str__(self):
        return f'{self.id} - {self.title} - {self.type}'

    def save(self, *args, **kwargs):
        if self.title_en is None:
            self.title_en = translator.translate(self.title)
        if self.slug is None:
            self.slug = slugify(self.title_en)
        return super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-created_at']


