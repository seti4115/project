from django.db import models

class SiteSettings(models.Model):
    title = models.CharField(max_length=100, verbose_name="عنوان سایت")
    url = models.URLField(verbose_name="آدرس سایت")
    logo = models.ImageField(verbose_name="لوگو")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="ساخته شده در")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="اپدیت شده در")
    about = models.TextField(blank=True, verbose_name="درباره ما")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    contact = models.TextField(blank=True, verbose_name="ارتباط با ما")
    gmail = models.TextField(blank=True, verbose_name="جیمیل")
    phone = models.TextField(blank=True, verbose_name="شماره تلفن")
    address = models.TextField(blank=True, verbose_name="آدرس")
    manager = models.TextField(blank=True, verbose_name="مدیر عامل")
    is_active = models.BooleanField(default=False, verbose_name="وضعیت فعال بودن")


    def __str__(self):
        return f"{self.pk}" + " - " + self.title

    def save(self, *args, **kwargs):
        if self.is_active:
            SiteSettings.objects.exclude(pk=self.pk).update(is_active=False)

        return super().save(*args, **kwargs)


    class Meta:
        ordering = ('-is_active',)
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'

