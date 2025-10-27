from django.contrib import admin
from persiantools.jdatetime import JalaliDate, JalaliDateTime

from product.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'price', 'production_date_jalali', 'expiration_date_jalali', 'is_active', 'updated_at_jalali']
    prepopulated_fields = {'slug': ('title_en',)}

    def production_date_jalali(self, obj):
        jdt = JalaliDate.to_jalali(obj.production_date)
        return jdt.strftime("%Y/%m/%d")

    def expiration_date_jalali(self, obj):
        jdt = JalaliDate.to_jalali(obj.expiration_date)
        return jdt.strftime("%Y/%m/%d")

    def updated_at_jalali(self, obj):
        jdt = JalaliDateTime.to_jalali(obj.updated_at)
        return jdt.strftime("%H:%M  %Y/%m/%d")

    production_date_jalali.short_description = 'تاریخ تولید'
    expiration_date_jalali.short_description = 'تاریخ انقضا'
    updated_at_jalali.short_description = 'ویرایش شده در'
